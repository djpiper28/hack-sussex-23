import dotenv
import audio_library.audio_lib as audio
import requests
import os
import json
from flask import Flask, redirect, request

app = Flask(__name__)

dotenv.load_dotenv()

redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
settingsFile = "../settings.json"


@app.route("/callback", methods=["POST"])
def callback() -> str:
    auth_code = request.args.get("auth_code")
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
        auth=(client_id, client_secret),
    )
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]

    with open(settingsFile, 'w') as f:
        json.dump({"access_token": access_token,
                  "refresh_token": refresh_token}, f)

    return "ok, now go away."


@app.route("/", methods=["GET", "POST"])
def hello() -> str:
    scope = ["user-read-playback-state",
             "user-modify-playback-state", "app-remote-control"]
    return redirect(f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={' '.join(scope)}", code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6666)
