import os
from re import sub
from twitter import *
from dotenv import dotenv_values
config = dotenv_values(".env")
from PIL import Image
import requests
from io import BytesIO

t = Twitter(
    auth=OAuth(config['TWITTER_ACCESS_TOKEN'], config['TWITTER_ACCESS_SECRET'], config['TWITTER_API_KEY'], config['TWITTER_API_SECRET']))

def tweet_stream(stream):
    hashtags = ""
    for tag in stream['tags']:
        hashtags += "#" + camel_case(tag) + " "

    tweet = f"Assista | {stream['title']} | https://brstreamers.dev/to/{stream['user_name']} \n #twitch #programacao #livestream"
    tweet_image(stream["avatar_url"], tweet)


def tweet_image(url, message):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        
        
        with open(filename, "rb") as imagefile:
            imagedata = imagefile.read()
        # - then upload medias one by one on Twitter's dedicated server
        #   and collect each one's id:
        t_upload = Twitter(domain='upload.twitter.com',
            auth=OAuth(config['TWITTER_ACCESS_TOKEN'], config['TWITTER_ACCESS_SECRET'], config['TWITTER_API_KEY'], config['TWITTER_API_SECRET']))
        
        # id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
        
          
        # t.statuses.update(media_ids=id_img1, status=message)
        os.remove(filename)
    else:
        print("Unable to download image")


def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])