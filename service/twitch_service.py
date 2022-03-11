import os
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch

load_dotenv()
twitch = Twitch(os.environ('CLIENT_ID'), os.environ('CLIENT_SECRET'))
streams_map = dict()


def get_streams():
    games = twitch.get_games(names=['Software and Game Development'])
    game_id = games['data'][0]['id']
    streams = twitch.get_streams(language="pt", game_id=game_id)
    streams_list = []
    for stream in streams['data']:
        twitch_user = get_streamer(stream['user_id'])
        user_map = {}
        user_map["user_name"] = stream['user_name']
        user_map["title"] = stream['title']
        user_map["started_at"] = stream['started_at']
        user_map['avatar_url'] = twitch_user['profile_image_url']
        
        tags = get_tags(stream['tag_ids'])
        user_map['tags'] = tags
        streams_list.append(user_map)
    return streams_list


def get_tags(tag_ids):
    tags = twitch.get_all_stream_tags(tag_ids=tag_ids)
    tags_list = []
    for tag in tags['data']:
        tags_list.append(tag['localization_names']['pt-br'])
    return tags_list



def get_streamer(id):
    return twitch.get_users(user_ids=[id])['data'][0]
