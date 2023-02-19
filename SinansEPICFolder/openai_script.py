import openai
import news_scraper as scraper
import dotenv
import audio_library.audio_lib as audio
import time
import random


def create_waffle(article_text, article_number):

    combined_text = (
        article_text[article_number]["title"]
        + ". "
        + article_text[article_number]["description"]
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Rewrite this in the form of an aggressive radio show:\n\n"
        + combined_text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
    )
    short_text = response.choices[0].text.strip()
    return short_text


def get_voice() -> str:
    VOICES = [audio.DANNY, audio.LEO, audio.SINAN]
    return VOICES[random.randint(0, len(VOICES) - 1)]


if __name__ == "__main__":
    dotenv.load_dotenv()

    while 1:
        try:
          print("Scraping")
          article_text = scraper.BBC().get_home_articles()
          article_number = random.randint(0, len(article_text)-1)
          settings = audio.get_audio_settings()
          audio_importer = audio.AudioImporter(settings)
          audio_importer.add_program_to_queue(
               audio_importer.add_program(
                 "Danny News or Leo News - WHOO KNOWS",
                 audio_importer.tts(
                      create_waffle(article_text, article_number), get_voice() 
                 ),
                )
          )

          time.sleep(60 * 10)
        except Exception as e:
            print(e)
