import psycopg2
import os

DATABASE_SQL = """
create table program (
  id integer primary key default nextval('next_id_seq'),
  name text not null,
  audio_data bytea not null
);

create table music (
  id integer not null references(program.id) default nextval('next_id_seq'),
  genre text not null
);

create index on music(genre);

create table queue (
  pos integer primary key default nextval('next_id_seq'),
  program_id integer not null references(program.id)
);
"""


class AudioImporterSettings:
    def __init__(self, username: str, password: str, db: str, host: str, port: str):
        self.username = username
        self.password = password
        self.db = db
        self.host = host
        self.port = port

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
        os.getenv("ELEVEN_LABS_KEY")
    )


class AudioImporter:
    def __init__(self, settings: AudioImporterSettings):
        self.settings = settings

    def tts(self, text: str) -> bytes:
       return None 

    def add_program(self, name: str, audio: bytes) -> int:
        return 1

    def add_music(self, name: str, audio: bytes, genre: str) -> int:
        return 1

    def add_program_to_queue(self, id: int):
        pass
