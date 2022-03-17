'''mainモジュール.'''
import os
import tweepy
import logging

from typing import Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.encoders import jsonable_encoder

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

bearer_token = os.getenv('bearer_token')
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

# サーバー
name = ''
root_path = os.getenv('ROOT_PATH', '')

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=f'{name} API',
    root_path=root_path
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['*'],
)

logging.basicConfig(level=logging.INFO)


@app.get('/{tag}', response_class=ORJSONResponse)
@limiter.limit("10/minute")
def getTweet(request: Request,
             tag: str,
             max_result: Optional[int] = 10,
             has_image: Optional[bool] = True) -> ORJSONResponse:
    '''Tweetを取得する.'''
    if tag.strip() == "":
        return ORJSONResponse(
            status_code=400,
            content={'detail': 'No hashtag specified'})

    query = f'(#{tag}) {"has:images" if has_image else ""} -is:retweet'
    print(query)

    client = tweepy.Client(
        bearer_token,
        consumer_key,
        bearer_token,
        access_token,
        access_token_secret
    )

    tweets = client.search_recent_tweets(
        query,
        max_results=max_result)

    result = []

    for t in tweets[0]:
        logging.info('----------------------------------------------------')
        logging.info('id %r' % t.id)
        logging.info('tweet %r' % print(t.text))
        ret = client.get_tweet(t.id,
                               expansions=['attachments.media_keys'],
                               media_fields=['preview_image_url', 'url'])
        if len(ret) > 0:
            if 'media' in ret[1] and ret[1]['media'] is not None:
                for media in ret[1]['media']:
                    if 'url' in media:
                        logging.info('url: %r' % media['url'])
        result.append(ret)

    return ORJSONResponse(content=jsonable_encoder(result))
