
from ctypes import sizeof
from dotenv import dotenv_values
from crontab import CronTab
from twitchAPI.twitch import Twitch
import schedule
import time

from service.twitch_service import get_streams
from service.twitter_service import tweet_stream

print('Starting Bot...')

config = dotenv_values(".env")
twitch = Twitch(config['CLIENT_ID'], config['CLIENT_SECRET'])
streams_map = dict()

streams_map = {}


def job():
    streams = get_streams()
    for stream in streams:
        if stream['user_name'] not in streams_map or streams_map[stream['user_name']] != stream['started_at']:
            try:
                streams_map[stream['user_name']] = stream['started_at']
                tweet_stream(stream)
                print(f'Twitting {stream["user_name"]} stream...')
            except Exception as e:
                print(f'Couldnt Twit {stream["user_name"]} stream...')


schedule.every(5).minutes.do(job)
print('Bot Scheduled...')

while True:
    schedule.run_pending()
    time.sleep(1)
