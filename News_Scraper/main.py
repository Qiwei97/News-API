from fastapi import FastAPI
from fastapi_restful.tasks import repeat_every
from News_Scraper.utils import generate_news
import json

app = FastAPI()

@app.get("/")
async def upload_news():
    with open('News_Scraper/data/news.json') as f:
        result = json.load(f)
    return result

@repeat_every(seconds = 5 * 60)
def update_news():
    df = generate_news(period='1M', category='Tech')
    df.to_json('News_Scraper/data/news.json', orient='records')