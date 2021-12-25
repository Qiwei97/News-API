from GoogleNews import GoogleNews
from newspaper import Article, Config
import pandas as pd
import time
import numpy as np
import nltk

config = Config()
config.MAX_SUMMARY_SENT = 2
config.MIN_WORD_COUNT = 200

def generate_news(period='3d', category='Health'):

    # Scrape from Google News
    print("Collecting Latest News...")
    googlenews = GoogleNews(period=period, region='SG')
    googlenews.search(category)

    for i in range(3):
        googlenews.get_page(i)
        time.sleep(2)

    df = pd.DataFrame(googlenews.result()).dropna()
    df = df.drop_duplicates(['title']).reset_index(drop = True)
    df.datetime = pd.to_datetime(df.datetime).astype(str)
    df = df.drop(columns = ['date'])

    assert len(df) > 0

    # Download Articles
    print("Downloading Articles...")
    news = []
    for ind in df.index:
        try:
            article_dict = {}
            article = Article(df['link'][ind], config=config)
            article.download()
            article.parse()
            article.nlp()
            article_dict['Date'] = df['datetime'][ind]
            article_dict['Media'] = df['media'][ind]
            article_dict['Link'] = df['link'][ind]
            article_dict['Title'] = article.title
            article_dict['Article'] = article.text
            article_dict['Summary'] = article.summary.replace('\n', ' ')
            article_dict['Image'] = article.top_image
            news.append(article_dict)
            time.sleep(3)
        except:
            pass

    news_df = pd.DataFrame(news)
    # Remove erratic articles
    news_df = news_df[news_df.Article.str.len() > 200]
    # Catch cases asking for sign up
    news_df.Summary = news_df.Summary.str.split('.').apply(lambda x: x.pop(0) if ('sign' in x[0]) or ('Sign' in x[0]) else x)
    # Control summary word count
    news_df.Summary = news_df.Summary.str.join('.').str.split().apply(lambda x: x[:30]).str.join(' ') + '...'
    news_df.replace('', np.nan, inplace=True)
    news_df = news_df.dropna()
    print(len(news_df), " Articles Found.")

    return news_df