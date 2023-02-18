import psycopg2
import os
import eleven_labs
import subprocess

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
            user=self.user,
            password=self.passowrd,
            host=self.host,
            port=self.port,
        )
        return conn


def get_audio_settings() -> AudioImporterSettings:
    return AudioImporterSettings(
        os.getenv("DB_USER"),
        os.getenv("DB_PASS"),
        os.getenv("DB_NAME"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("ELEVEN_LABS_KEY"),
    )


class AudioImporter:
    def __init__(self, settings: AudioImporterSettings):
        self.settings = settings

    def tts(self, text: str, voice_id: str) -> bytes:
        return eleven_labs.eleven_labs_tts(text, self.settings.el_key, voice_id)

    def add_program(self, name: str, audio: bytes) -> int:
        return 1

    def add_music(self, name: str, audio: bytes, genre: str) -> int:
        return 1

    def add_program_to_queue(self, id: int):
        pass

        """
if __name__ == "__main__":
    file = "output.mp3"
    settings = get_audio_settings()
    f = open(f"{file}", "wb")
    f.write(eleven_labs.eleven_labs_tts("Testing 123", settings.el_key, "21m00Tcm4TlvDq8ikWAM"))
    f.close()
    
    subprocess.call(f"vlc {file}", shell=True)
        """
