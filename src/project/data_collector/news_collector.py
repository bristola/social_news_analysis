from newsapi.newsapi_client import NewsApiClient
from newspaper import Article, fulltext
from data_collector import Data_Collector

# pip install newsapi-python
# pip install newspaper3k

class News_Collector(Data_Collector):

    def __init__(self, key):
        self.api = NewsApiClient(api_key=key)
        super().__init__('news.txt')


    def search(self, topic):
        json = self.api.get_everything(q=topic, language='en', sort_by='relevancy')
        articles = json['articles']
        news = list()
        for article in articles:
            print(article['url'])
            a = Article(article['url'])
            a.download()
            text = fulltext(a.html)
            news.append(text)
        return news

    def run(self, topic):
        news = self.search(topic)
