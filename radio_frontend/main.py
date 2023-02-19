from pynput.keyboard import Controller, Key

import subprocess
import psycopg2
import dotenv
import time
import traceback
import audio_library.audio_lib as audio

TMP_FILE = "tmp.mp3"


def get_next(settings: audio.AudioSettings) -> bytes:
    c = settings.get_connection()
    cur = c.cursor()
    cur.execute(
        """select queue.pos, program.name, program.audio_data
        from program, queue 
        where program.id = queue.program_id 
        order by queue.pos asc 
        limit 1;"""
    )
    tmp = cur.fetchone()
    print(len(tmp))
    pos = tmp[0]
    name = tmp[1]
    ret = tmp[2]

    cur.execute("delete from queue where pos = %s;", (pos,))
    c.commit()
    c.close()

    print(f"Found {name} in pos {pos} with size {len(ret) / 1024 / 1024} MiB")
    return ret


def main(settings: audio.AudioSettings) -> None:
    keyboard = Controller()
    while True:
        try:
            data: bytes = get_next(settings)
            f = open(TMP_FILE, "wb")
            f.write(data)
            f.close()

            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
            time.sleep(0.1)
            subprocess.run(f"mpv {TMP_FILE}", shell=True, check=True)
            time.sleep(0.1)
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
        except:
            print("Shit is fucked")
            traceback.print_exc()
            time.sleep(1)


if __name__ == "__main__":
    dotenv.load_dotenv()
    settings: audio.AudioSettings = audio.get_audio_settings()
    main(settings)
