import dotenv
import audio_library.audio_lib as audio
import requests
import openai
from flask import Flask, request

app = Flask(__name__)
audio_importer = None


def queue_response(text: str) -> None:
    global audio_importer
    # Send to gpt 3
    print(f"Responding to {text}")
    response = openai.Completion.create(
        engine="davinci",
        prompt='Respond to the following text message to Crackle FM, being aggresive to the sender and, defending our music choices "{text}"',
        temperature=0.9,
        max_tokens=256,
    )
    out_text = response.choices[0].text.strip()

    # Add to database
    audio_importer.add_program_to_queue(
        audio_importer.add_program(
            f"SMS Message Response for {text}",
            audio_importer.tts(out_text, audio.PIERS_MORGAN),
        )
    )


@app.route("/", methods=["GET", "POST"])
def func() -> str:
    queue_response(request.get_data().decode("UTF-8"))
    return "it's someone else's problem now"


if __name__ == "__main__":
    dotenv.load_dotenv()
    settings = audio.get_audio_settings()
    audio_importer = audio.AudioImporter(settings)
    app.run(host="0.0.0.0", port=6969)
