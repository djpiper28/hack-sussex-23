import requests
from bs4 import BeautifulSoup

class BBC:
    def __init__(self):
        self.url = "http://feeds.bbci.co.uk/news/rss.xml"
        home = requests.get(self.url)
        self.soup = BeautifulSoup(home.content, features="xml")
        #self.body = self.get_article_body()
        
    def get_home_articles(self):
        home_page = self.soup.findAll("item") # Scrapes the URL home page
        all_links = [] # List to store all the links from the home page
        for article_link in home_page: # For loop that appends the title of each story
            story = {} # Dictionary for each story
            story["title"] = article_link.title.text
            story["link"] = article_link.link.text
            all_links.append(story)

        return all_links

    def get_article_body(self):
        text = []

        for read_article in self.get_home_articles():
            article = requests.get(read_article["link"])
            soup = BeautifulSoup(article.content, 'html.parser')
            try: # A try/catch was used to skip the articles with no text to scrape (usually just the ones with just videos) - (im so very sorry)
                if "sport" in read_article["link"]:
                    body = soup.find(class_='gel-layout__item gel-2/3@l')
                    text.append(self.get_sentences(body))
                else:
                    body = soup.find(class_='ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6')
                    text.append(self.get_sentences(body))
            except:
                print("")

        return text

    def get_sentences(self, body):
        article_text = []
        for p in body.find_all("p"):
            if ("Watch: " not in p.text) and ("This video can not be played" not in p.text):
                article_text.append(p.text)
        return article_text

parse_bbc = BBC()
print(parse_bbc.get_article_body())