import os
import json
from googleapiclient.discovery import build

env_var=os.environ
env_var['YT_API_KEY'] = 'AIzaSyABL6-p6geWeiWBdAScLTLYEmxSyWLjtZk'

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id=channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscribers = None
        self.video_count = None
        self.view_count = None

        api_key: str = os.getenv('YT_API_KEY')
        youtube = self.get_service(api_key)
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=self.channel_id
        )

        response = request.execute()
        if response['items']:
            channel_data = response['items'][0]
            self.title = channel_data['snippet']['title']
            self.description = channel_data['snippet']['description']
            self.url = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscribers = int(channel_data['statistics']['subscriberCount'])
            self.video_count = int(channel_data['statistics']['videoCount'])
            self.view_count = int(channel_data['statistics']['viewCount'])


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(f"Название канала: {self.title}")
        print(f"Описание канала: {self.description}")
        print(f"Ссылка на канал: {self.url}")
        print(f"Количество подписчиков: {self.subscribers}")
        print(f"Количество видео: {self.video_count}")
        print(f"Общее количество просмотров: {self.view_count}")

    @classmethod
    def get_service(cls, api_key: str):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename: str) -> None:
        """Сохраняет в файл значения атрибутов экземпляра Channel в формате JSON."""
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, 'w') as f:
            json.dump(data, f)