import psycopg2
import os
import subprocess
import dotenv
import requests
import subprocess
import openai

TMP_FILE = f"tmp-{os.getpid()}.mp3"

"""
This method will contact the eleven labs api and, use their speech synthesis to generate
an mp3 file from the given input, this can then be saved in the database
"""


def eleven_labs_tts(text: str, api_key: str, voice_id: str) -> bytes:
    url: str = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    settings = dict()
    settings["text"] = text

    voice_settings = dict()
    voice_settings["stability"] = 0
    voice_settings["similarity_boost"] = 0
    settings["voice_settings"] = voice_settings

    headers = {
        "xi-api-key": api_key,
        "accept": "*/*",
        "Content-Type": "application/json",
    }

    r = requests.post(url, json=settings, headers=headers)
    if r.status_code != 200:
        raise RuntimeError(r.text)

    print(f"Generated '{text}' using {voice_id}")
    return r.content


PIERS_MORGAN = "ghs8Pp3EHJvOdXnIE00e"
JORDAN_PETERSON = "CVyI62Pgl2ns5yHkp9Th"
DANNY = "Qm8ECFgftVCqQGCGNfOO"
LEO = "gaq1ichFbfkQpeOEoQIE"
SINAN = "myCqH5RBENXISuh1jhFL"


class AudioSettings:
    def __init__(
        self,
        username: str,
        password: str,
        db: str,
        host: str,
        port: str,
        el_key: str,
        gpt_key: str,
    ):
        self.username = username
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        self.el_key = el_key
        self.gpt_key = gpt_key
        openai.api_key = self.gpt_key

    def get_connection(self):
        conn = psycopg2.connect(
            database=self.db,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        print(f"Connected to {self.host}:{self.port}")
        return conn


def get_audio_settings() -> AudioSettings:
    return AudioSettings(
        os.getenv("DB_USER"),
        os.getenv("DB_PASS"),
        os.getenv("DB_NAME"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("EL_API"),
        os.getenv("GPT_KEY"),
    )


class AudioImporter:
    def __init__(self, settings: AudioSettings):
        self.settings = settings

    def __get_id(self) -> int:
        c = self.settings.get_connection()
        cur = c.cursor()
        cur.execute("select nextval('serial_num');")
        ret = cur.fetchall()[0][0]
        c.close()
        print(f"New id {ret}")
        return ret

    def tts(self, text: str, voice_id: str) -> bytes:
        return eleven_labs_tts(text, self.settings.el_key, voice_id)

    def add_program(self, name: str, audio: bytes) -> int:
        id = self.__get_id()
        c = self.settings.get_connection()
        c.cursor().execute(
            "insert into program (id, name, audio_data) values (%s, %s, %s);",
            (id, name, audio),
        )
        c.commit()
        c.close()
        print(f"Added {name} to database with {len(audio) / 1024 / 1024} MiB")
        return id

    def add_music(self, name: str, audio: bytes, genre: str) -> int:
        id = self.add_program(name, audio)

        c = self.settings.get_connection()
        c.cursor().execute(
            "insert into music (id, genre) values (%s, %s);", (id, genre)
        )
        c.commit()
        c.close()
        print(f"Added {name}({genre}) to tracks")

        return id

    def add_program_to_queue(self, pid: int) -> None:
        c = self.settings.get_connection()
        id = self.__get_id()
        c.cursor().execute(
            "insert into queue (pos, program_id) values (%s, %s);", (id, pid)
        )
        c.commit()
        c.close()
        print(f"Added {pid} to the queue")


if __name__ == "__main__":
    dotenv.load_dotenv()
    settings = get_audio_settings()
    audio = AudioImporter(settings)
    for i in range(1100, 1200):
        try:
            audio.add_program_to_queue(i)
        except:
            pass
