import os
import time
from datetime import date, timedelta
import requests
from moviepy.editor import VideoFileClip
import moviepy.editor
import pathlib

# Twitch API authentication

with open('client_id', 'r') as ci:
    client_id = ci.read()
with open('client_secret', 'r') as cs:
    client_secret = cs.read()

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

# Get Twitch clips from the previous day
def info():
    yesterday = date.today() - timedelta(1)
    yesterday = str(yesterday)
    yesterday_start = yesterday+'T00:00:00Z'
    yesterday_end = yesterday+'T23:59:59Z'
    return yesterday_start, yesterday_end

def get_clips(start, end):
    clips = requests.get(f'https://api.twitch.tv/helix/clips?broadcaster_id=461774409&first=20&started_at={start}&ended_at={end}', headers=headers)
    clips_data = clips.json()
    return clips_data

# Download Twitch clips
def download_clips(data):
    title = data['data'][0]['title']
    clip_to_download = []
    for clip in data['data']:
        clip_to_download.append(clip['url'])
    for link in clip_to_download:
        os.system(f'twitch-dl download -q 1080p {link}')
    return title

# Prepare video files for concatenation
def preparing_videos():
    files_to_montage = []
    for file in sorted(pathlib.Path('.').iterdir(), key=os.path.getmtime):
        file = str(file)
        if file.endswith('.mp4'):
            files_to_montage.append(file)
    return files_to_montage

# Concatenate video files
def creating_video(files):
    fragments = []
    for file in files:
        fragments.append(VideoFileClip(file).subclip())
    video = moviepy.editor.concatenate_videoclips(fragments)
    video.write_videofile("youtube.mp4")
    return None

# Upload video to YouTube
def upload(title):
    os.system(f'python upload_video.py --file="youtube.mp4" --title="{title} | Daily Soup of Kret" --description="Najlepsze shoty z ostatniego dnia" --keywords="chess, szachy, xntentacion, stream, shorts" --category="24" --privacyStatus="public"')
    return None

# Delete downloaded clips
def delete_videos():
    for file in os.listdir("."):
        if file.endswith(".mp4"):
            os.remove(os.path.join(".", file))
    print('videos were deleted')
    return None

# Run the script in an infinite loop
if __name__ == "__main__":
    while True:
        start, end = info()
        clips = get_clips(start, end)
        title = download_clips(clips)
        files = preparing_videos()
        creating_video(files)
        upload(title)
        delete_videos()
        time.sleep(86400) # wait 24 hours before running again