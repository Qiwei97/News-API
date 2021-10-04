from fastapi import FastAPI
from News_Scraper.utils import generate_news
import json

app = FastAPI()

@app.get("/")
async def upload_news():
    with open('News_Scraper/data/news.json') as f:
        result = json.load(f)
    return result

@app.get("/update_news/")
async def update_news():
    df = generate_news(period='1M', category='Tech')
    df.to_json('News_Scraper/data/news.json', orient='records')
    return('News Updated.')