from fastapi import FastAPI
from dotenv import load_dotenv
from datetime import datetime as dt
from pytz import timezone
import sys
import i18n
import os
import urllib.request
import requests
import json
import time

load_dotenv(verbose=True)

from kaggle.api.kaggle_api_extended import KaggleApi

i18n.set('locale', os.environ.get('LOCALE'))
i18n.load_path.append('./locale')

api = KaggleApi()
api.authenticate()

app = FastAPI()

def post_discord(message):
    requests.post(os.environ.get('DISCORD_WEBHOOK_URL'), {'content': message})

@app.get("/")
def hello():
    return {'hello': 'world'}

@app.get('/post_kaggle_competitions')
def post_kaggle_competitions():
    now = dt.now()
    now = now.astimezone(timezone('UTC'))
    post_discord(i18n.t('kaggle.hi', hour=now.hour))
    
    competitions_list = api.competitions_list()
    for competition in competitions_list:
        if getattr(competition, 'awardsPoints') and not getattr(competition, 'submissionsDisabled'):
            deadline = getattr(competition, 'deadline')
            deadline = deadline.astimezone(timezone('UTC'))
            diff = deadline - now
            if diff.days > 0:
                post_discord('{}: {}'.format(i18n.t('kaggle.to_go', days=diff.days), getattr(competition, 'title')))
                time.sleep(1)
