import datetime

import isodate

import channel
from src.video import PLVideo
from src.config import get_api_key
from googleapiclient.discovery import build

class PlayList(PLVideo):
    def __init__(self, plist_id):
        super().__init__('some_video_id', plist_id)
        self.plist_id = plist_id
        self.videos = []
        self.title = None
        self.url = None
        self.load_playlist_info()  # Метод для загрузки информации о плейлисте

        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.load_playlist_info['items']]


        self.video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                                   id=','.join(self.video_ids)
                                                                   ).execute()


    def load_playlist_info(self):
        api_key = get_api_key()
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist_info = youtube.playlists().list(part='snippet', id=self.plist_id).execute()

        if 'items' in playlist_info:
            playlist_data = playlist_info['items'][0]
            self.title = playlist_data['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.plist_id}"

    def add_video(self, video):
        self.videos.append(video)

    def remove_video(self, video):
        self.videos.remove(video)

    @property
    def total_duration(self):
        self.video_response = channel.Channel.get_service().videos().list(part='contentDetails', id=', '.join(self.plist_id)).execute()
        print(self.video_response)
        duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

        # total_duration_seconds = sum(video.duration.total_seconds() for video in video_response['items'])
        # return datetime.timedelta(seconds=total_duration_seconds)

    def show_best_video(self):
        best_video = max(self.videos, key=lambda video: video.like_video)
        return best_video.url

pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
duration = pl.total_duration
print(str(duration)) #== "1:49:52"

