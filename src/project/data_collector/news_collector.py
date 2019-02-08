from newsapi.newsapi_client import NewsApiClient
from newspaper import Article, fulltext
from data_collector import Data_Collector

# pip install newsapi-python
# pip install newspaper3k

class News_Collector(Data_Collector):

    def __init__(self, key):
        self.api = NewsApiClient(api_key=key)
        super().__init__('data.txt')


    def search(self, topic, max=1, c=100):
        """
        Takes the input topic and collects next 100 news articles based on max
        paramter. Collects article text and author.
        """
        # Searches for headlines and gets article data
        json = self.api.get_everything(q=topic, language='en', sort_by='relevancy', page=max, page_size=c)
        articles = json['articles']
        news = list()
        for article in articles:
            # Takes the URL of the article and downloads the full content
            a = Article(article['url'])
            a.download()
            # If download failed, continue to next article
            try:
                # Takes the whole article's text and adds it to output
                text = fulltext(a.html)
                current = dict()
                current['text'] = text
                current['author'] = article['author']
                news.append(current)
            except Exception as e:
                pass
        return news, max+1


    def create_strings(self, data):
        """
        Takes input data and gets it into a format which will be written to a
        file.
        """
        out_articles = list()
        for article in data:
            # Clean article data
            out = article['text'].replace("\n","").replace("Advertisement","")
            out_articles.append(out)
        return out_articles


    def run(self, topic, iterations):
        """
        Runs the collection of news articles on the given topic the input number
        of times. Each time will make sure that it is a unique set of news
        articles.
        """
        page = 1
        news_paper = list()
        for i in range(0, iterations):
            # Collect data, and move on to next page on return
            news, page = self.search(topic, max=page)
            # Add results to final output
            news_paper.extend(news)
        # Prepare and write data to file
        news_paper = self.filter_authors(news_paper)
        news_paper = self.create_strings(news_paper)
        self.write_to_file(news_paper)
