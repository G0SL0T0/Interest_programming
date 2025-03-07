from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

# Инициализация YouTube API
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Сбор комментариев под видео
def fetch_youtube_comments(video_id, count=10):
    comments = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=count,
        textFormat="plainText"
    ).execute()
    return [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in comments['items']]