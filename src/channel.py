import json
from googleapiclient.discovery import build
from src.config import get_api_key


class Channel:
    """Класс для ютуб-канала"""
    api_key = get_api_key()

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscribers = None
        self.video_count = None
        self.view_count = None

        self.request = self.get_service().channels().list(
            part="snippet,contentDetails,statistics",
            id=self.channel_id
        )

        response = self.request.execute()

        if response['items']:
            channel_data = response['items'][0]
            self.title = channel_data['snippet']['title']
            self.description = channel_data['snippet']['description']
            self.url = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscribers = int(channel_data['statistics']['subscriberCount'])
            self.video_count = int(channel_data['statistics']['videoCount'])
            self.view_count = int(channel_data['statistics']['viewCount'])

    def __str__(self):
        """возвращает название и ссылку на канал"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """складывание двух каналов между собой по количеству подписчиков"""
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        """вычитание двух каналов между собой по количеству подписчиков"""
        return self.subscribers - other.subscribers

    def __gt__(self, other):
        """сравнение «больше» > двух каналов между собой по количеству подписчиков"""
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        """сравнение «больше или равно» >= двух каналов между собой по количеству подписчиков"""
        return self.subscribers >= other.subscribers

    def __lt__(self, other):
        """сравнение «меньше» < двух каналов между собой по количеству подписчиков"""
        return self.subscribers < other.subscribers

    def __le__(self, other):
        """сравнение «меньше или равно»  <= двух каналов между собой по количеству подписчиков"""
        return self.subscribers <= other.subscribers

    def __eq__(self, other):
        """сравнение  "равенство" == двух каналов между собой по количеству подписчиков"""
        return self.subscribers == other.subscribers

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(f"Название канала: {self.title}")
        print(f"Описание канала: {self.description}")
        print(f"Ссылка на канал: {self.url}")
        print(f"Количество подписчиков: {self.subscribers}")
        print(f"Количество видео: {self.video_count}")
        print(f"Общее количество просмотров: {self.view_count}")

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

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