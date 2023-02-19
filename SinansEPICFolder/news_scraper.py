import requests
import dotenv
import audio_library.audio_lib as audio
from bs4 import BeautifulSoup


class BBC:
    def __init__(self):
        self.url = "http://feeds.bbci.co.uk/news/rss.xml"
        home = requests.get(self.url)
        self.soup = BeautifulSoup(home.content, features="xml")
        # self.body = self.get_article_body()

    def get_home_articles(self):
        home_page = self.soup.findAll("item")  # Scrapes the URL home page
        all_links = []  # List to store all the links from the home page
        for article_link in home_page:  # For loop that appends the title of each story
            story = {}  # Dictionary for each story
            story["title"] = article_link.title.text
            story["link"] = article_link.link.text
            story["description"] = article_link.description.text
            all_links.append(story)

        return all_links

    def get_body_for_article(self, read_article):
        article = requests.get(read_article["link"])
        soup = BeautifulSoup(article.content, "html.parser")
        try:  # A try/catch was used to skip the articles with no text to scrape (usually just the ones with just videos) - (im so very sorry)
            if "sport" in read_article["link"]:
                body = soup.find(class_="gel-layout__item gel-2/3@l")
                return self.get_sentences(body)
            else:
                body = soup.find(class_="ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6")
                return self.get_sentences(body)
        except:
            return None

    def get_article_body(self):
        text = []

        for read_article in self.get_home_articles():
            text.append(self.get_body_for_article(read_article))

        return text

    def get_sentences(self, body):
        article_text = []
        for p in body.find_all("p"):
            if ("Watch: " not in p.text) and (
                "This video can not be played" not in p.text
            ):
                article_text.append(p.text)
        return article_text


def get_news():
    parse_bbc = BBC()
    articles = parse_bbc.get_home_articles()

    ret = []
    for article in articles[0:10]:
        ret.append(article)  # parse_bbc.get_body_for_article(article))
    return ret


if __name__ == "__main__":
    dotenv.load_dotenv()
    settings = audio.get_audio_settings()
    audio_importer = audio.AudioImporter(settings)
    for article in get_news():
       title = "More breaking news!! " + article["title"]
       audio_importer.add_program_to_queue(
           audio_importer.add_program(
               "Danny's test audio_importer", audio_importer.tts(title, audio.DANNY)
           )
       )
