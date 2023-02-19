import dotenv
import audio_library.audio_lib as audio
import requests
import openai
from flask import Flask, request
from threading import Thread

app = Flask(__name__)
audio_importer = None


def replace_naughty_words(text: str) -> str:
    with open("/home/danny/naughty_words.txt") as f:
        for line in f:
            text = text.replace(line, "-")
    return text


# The topic should be a string that is the topic of the radio show
def createRadioShow(topic: str):
    global audio_importer
    print(f"Centering radio show around {topic}")
    prompt = f"""Jordan Peterson and Piers Morgan are hosting a radio show, and they're talking about {topic}, their guest, Danny Piper who is a member of the british computing society and, Leo who is a C++ developer and avid windows user.

    Jordan:"""

    # Send to gpt 3
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.96,
        max_tokens=512,
    )
    out_text = replace_naughty_words(response.choices[0].text.strip())
    print(f"Chatting the following arse: \n\n{out_text}")
    out_text = prompt + out_text
    # split the text by new lines and get whoever is speaking

    splitText = textSplitter(out_text)
    speakerToAudio(splitText)

    for i in range(0, 5):
        # if there are over 5 messages in the text, we need to remove the old messages
        if len(list(filter(lambda x: ":" in x, out_text.split("\n")))) > 5:
            out_text = textRemoveOldMessages(out_text)

        res = openai.Completion.create(
            engine="davinci",
            prompt=out_text,
            temperature=0.94,
            max_tokens=512,
        )

        out_text = res.choices[0].text.strip()

        # split the text by new lines and get whoever is speaking
        splitText = textSplitter(out_text)
        # Now this uses the dictionary to generate the audio of whoever is speaking
        speakerToAudio(splitText)


def textSplitter(text):
    split = text.split("\n")
    # Filter out the empty strings
    split = list(filter(None, split))
    # Filter out out all the strings that don't have a colon in them
    split = list(filter(lambda x: ":" in x, split))
    # Now we have a list of strings, each string is a quote, we need to split the name from the quote
    # We can do this by splitting the string by the colon
    # We can then add the name and quote to a dictionary
    split = [i.split(":") for i in split]

    dictionary = {}
    for i in split:
        dictionary[i[0]] = i[1]

    return split


def textRemoveOldMessages(text):
    # we need to remove the old messages from the text, but we need to keep the initial prompt

    # First we need to split the text by new lines
    split = text.split("\n")

    prompt = split[0]

    # Now we need to filter out all the strings that don't have a colon in them

    split = list(filter(lambda x: ":" in x, split))

    # Let's now get only the last 5 messages from the list
    split = split[-5:]

    # Now we need to join the list back into a string
    split = "\n".join(split)

    # Now we need to add the prompt back to the start of the string

    split = prompt + "\n" + split

    return split


def speakerToAudio(splitText: list):
    # This function will take a speaker and return the audio of the speaker
    # We can do this by using the audio library
    voice = audio.PIERS_MORGAN

    # Let's now get the audio of whoever is speaking
    for i in splitText:
        if i[0] == "Jordan":
            voice = audio.JORDAN_PETERSON
        elif i[0] == "Danny":
            voice = audio.DANNY
        elif i[0] == "Piers":
            voice = audio.PIERS_MORGAN
        elif i[0] == "Leo":
            voice = audio.LEO

        # Add to database
        audio_importer.add_program_to_queue(
            audio_importer.add_program(
                "Interview segment",
                audio_importer.tts(i[1], voice),
            )
        )


def queue_response_normal(text: str) -> None:
    global audio_importer
    # Send to gpt 3
    print(f"Responding to {text}")
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Respond to the following text message, being aggresive to the sender and, defending our music choices: {text}",
        temperature=0.7,
        max_tokens=70,
    )
    out_text = replace_naughty_words(response.choices[0].text.strip())
    print(f"Chatting the following arse{out_text}")

    # Add to database
    audio_importer.add_program_to_queue(
        audio_importer.add_program(
            f"SMS Message Response for {text}",
            audio_importer.tts(out_text, audio.PIERS_MORGAN),
        )
    )


def queue_response(text: str) -> None:
    if text[0] == "?":
        createRadioShow(text[1:])
    else:
        queue_response_normal(text)


@app.route("/", methods=["GET", "POST"])
def func() -> str:
    t = Thread(target=queue_response, args=(request.get_data().decode("UTF-8"),))
    t.start()
    return "it's someone else's problem now"


if __name__ == "__main__":
    dotenv.load_dotenv()
    settings = audio.get_audio_settings()
    audio_importer = audio.AudioImporter(settings)
    app.run(host="0.0.0.0", port=6969)
