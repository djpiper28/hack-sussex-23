from spotipy.oauth2 import SpotifyOAuth

import spotipy
import subprocess
import dotenv
import time
import traceback
import os
import random
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
    if tmp is None:
        return None
    pos = tmp[0]
    name = tmp[1]
    ret = tmp[2]

    cur.execute("delete from queue where pos = %s;", (pos,))
    c.commit()
    c.close()

    print(f"Found {name} in pos {pos} with size {len(ret) / 1024 / 1024} MiB")
    return ret


SECONDS_TEXT_AD = 60 * 20


def main(settings: audio.AudioSettings) -> None:
    scope = "user-read-playback-state,user-modify-playback-state,app-remote-control"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
    last: int = 0

    while True:
        global paused
        paused = False
        try:
            if time.time() - last >= SECONDS_TEXT_AD:
                print("Advertising")
                last = time.time()
                ads = []
                for f in os.listdir():
                    if "call_in_" in f:
                        ads.append(f)
                ad = ads[random.randint(0, len(ads) - 1)]

                sp.pause_playback()
                paused = True
                time.sleep(0.1)
                subprocess.run(
                    f"mpv {ad}",
                    shell=True,
                    check=True,
                )
                time.sleep(0.1)

            data: bytes = get_next(settings)
            if data == None:
                time.sleep(1)
                continue
            sp.pause_playback()
            paused = True
            f = open(TMP_FILE, "wb")
            f.write(data)
            f.close()

            time.sleep(0.1)
            subprocess.run(
                f"ffmpeg-normalize tmp.mp3 -o out.mp3 -c:a libmp3lame && mv out.mp3 tmp.mp3 && mpv {TMP_FILE}",
                shell=True,
                check=True,
            )
            time.sleep(0.1)
        except:
            print("Shit is fucked")
            traceback.print_exc()
            time.sleep(1)
        if paused:
            try:
                sp.start_playback()
            except:
                traceback.print_exc()


if __name__ == "__main__":
    dotenv.load_dotenv()
    settings: audio.AudioSettings = audio.get_audio_settings()
    main(settings)
