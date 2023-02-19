import openai
import news_scraper as scraper

openai.api_key = ""

def create_waffle(article_text, article_number):

    combined_text = article_text[article_number]["title"] + ". " + article_text[article_number]["description"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Rewrite this in the form of an aggressive radio show hosted by Piers Morgan:\n\n" + combined_text,
        temperature = 0.7,
        max_tokens=256,
        top_p = 1
    )
    short_text = response.choices[0].text.strip()
    return (short_text)

if __name__ == "__main__":
    article_text = scraper.BBC().get_home_articles()
    article_number = 1
    print(create_waffle(article_text, article_number))