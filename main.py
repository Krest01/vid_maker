import requests
from datetime import date, timedelta
import os
from moviepy.editor import VideoFileClip


yesterday = date.today() - timedelta(1)
yesterday = str(yesterday)
yesterday_start = yesterday+'T00:00:00Z'
yesterday_end = yesterday+'T23:59:59Z'


client_id = '37zxvqwg12hts6aji5ucmd34h36pww'
client_secret = 'afw6htfiii1ipgogjuo722f2pln6o5'
streamer_name = 'xntentacion'


body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}


response = requests.post('https://id.twitch.tv/oauth2/token', body)
auth_token = response.json()


headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + auth_token['access_token'],
}


clips = requests.get(f'https://api.twitch.tv/helix/clips?broadcaster_id=461774409&first=20&started_at={yesterday_start}&ended_at{yesterday_end}', headers=headers)
clips_data = clips.json()


title = clips_data['data'][0]['title']
clip_to_download = []
for clip in clips_data['data']:
    clip_to_download.append(clip['url'])

for link in clip_to_download:
    os.system(f'twitch-dl download -q 1080p {link}')

def preparing_videos():
    files_to_montage = []
    for file in os.listdir('./'):
        if file.endswith('.mp4'):
            files_to_montage.append(file)
    return files_to_montage
