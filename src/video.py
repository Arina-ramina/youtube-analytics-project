from googleapiclient.discovery import build
from src.config import get_api_key
from googleapiclient.errors import HttpError


class Video:
    """Класс для ютуб-видео"""
    api_key = get_api_key()
    """Экземпляр инициализирует id канал. Дальше все данные будут подтягиваться по API."""

    def __init__(self, id_video):
        self.id_video = id_video
        self.name_video = None
        self.url_video = None
        self.view_video = None
        self.like_video = None

        try:
            self.request = self.get_service().videos().list(
                part="snippet,statistics",
                id=self.id_video
            )
            response = self.request.execute()

            if response['items']:
                video_data = response['items'][0]
                self.name_video = video_data['snippet']['title']
                self.url = f"https://www.youtube.com/watch?v={self.id_video}"
                self.view_video = int(video_data['statistics']['viewCount'])
                self.like_video = int(video_data['statistics']['likeCount'])
        except HttpError as e:
            self.name_video = self.url_video = self.view_video = self.like_video = None
            print(f"Ошибка при получении данных для видео {self.id_video}: {e}")



    def get_service(self):
        return build("youtube", "v3", developerKey=self.api_key)

    def __str__(self):
        return self.name_video


class PLVideo(Video):
    """Класс для видео, у которого есть плейлист."""

    def __init__(self, video_id: str, plist_id: str) -> None:
        """Инициализируется id видео и плейлист.
        @type plist_id: str
        """
        super().__init__(video_id)
        self.plist_id = plist_id
