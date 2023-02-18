import psycopg2
import os
import eleven_labs
import subprocess
import dotenv

PIERS_MORGAN = "3Ht7G75cBW4JaQld9TQI"
JORDAN_PETERSON = "B4emaEpL5FcK3fc2AX1f"
DANNY = "IlLo2Vy8UKY0YQ4muyjI"


class AudioImporterSettings:
    def __init__(
        self, username: str, password: str, db: str, host: str, port: str, el_key: str
    ):
        self.username = username
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        self.el_key = el_key

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


def get_audio_settings() -> AudioImporterSettings:
    return AudioImporterSettings(
        os.getenv("DB_USER"),
        os.getenv("DB_PASS"),
        os.getenv("DB_NAME"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("EL_API"),
    )


class AudioImporter:
    def __init__(self, settings: AudioImporterSettings):
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
        return eleven_labs.eleven_labs_tts(text, self.settings.el_key, voice_id)

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
    f = open("/home/danny/Downloads/Ram Ranch.wav", "rb")
    audio.add_program_to_queue(audio.add_program("Danny's test audio", f.read()))
    f.close()
