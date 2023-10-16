import datetime
import isodate
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
        self.api_key = get_api_key()  # Получаем API ключ
        self.video_response = None  # Инициализируем переменную

        # Загрузка информации о плейлисте
        self.load_playlist_info()

    def get_service(self):
        return build("youtube", "v3", developerKey=self.api_key)

    def load_playlist_info(self):
        youtube = self.get_service()
        playlist_info = youtube.playlists().list(part='snippet', id=self.plist_id).execute()

        if 'items' in playlist_info:
            playlist_data = playlist_info['items'][0]
            self.title = playlist_data['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.plist_id}"

    def get_video_ids(self):
        # Получаем список ID видеороликов в плейлисте
        if self.video_response is not None and 'items' in self.video_response:
            return [video['contentDetails']['videoId'] for video in self.video_response['items']]
        return []

    def update_video_info(self):
        # Получаем информацию о видеороликах в плейлисте и обновляем video_response
        youtube = self.get_service()
        video_ids = self.get_video_ids()
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        self.video_response = video_response

    @property
    def total_duration(self):
        # Получаем общую длительность видеороликов в плейлисте
        if self.video_response is not None and 'items' in self.video_response:
            duration = datetime.timedelta()
            for video in video_response['items']:
                # YouTube video duration is in ISO 8601 format
                iso_8601_duration = video['contentDetails']['duration']
                duration = isodate.parse_duration(iso_8601_duration)
                print(duration)
        return datetime.timedelta()

    def show_best_video(self):
        best_video = max(self.videos, key=lambda video: video.like_video)
        return best_video.url


pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
duration = pl.total_duration
print(duration)


