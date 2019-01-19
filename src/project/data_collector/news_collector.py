from newsapi.newsapi_client import NewsApiClient
from newspaper import Article, fulltext
from data_collector import Data_Collector

# pip install newsapi-python
# pip install newspaper3k

class News_Collector(Data_Collector):

    def __init__(self, key):
        self.api = NewsApiClient(api_key=key)
        super().__init__('news.txt')


    def search(self, topic, max=1, c=100):
        json = self.api.get_everything(q=topic, language='en', sort_by='relevancy', page=max, page_size=c)
        articles = json['articles']
        news = list()
        for article in articles:
            a = Article(article['url'])
            a.download()
            try:
                text = fulltext(a.html)
                current = dict()
                current['text'] = text
                current['author'] = article['author']
                news.append(current)
            except Exception as e:
                pass
        return news, max+1


    def create_strings(self, data):
        out_articles = list()
        for article in data:
            out = article['text'].replace("\n","").replace("Advertisement","")
            out_articles.append(out)
        return out_articles


    def run(self, topic, iterations):
        page = 1
        news_paper = list()
        for i in range(0, iterations):
            news, page = self.search(topic, max=page)
            news_paper.extend(news)
        news_paper = self.filter_authors(news_paper)
        news_paper = self.create_strings(news_paper)
        self.write_to_file(news_paper)
