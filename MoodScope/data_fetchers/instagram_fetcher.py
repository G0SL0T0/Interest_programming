from instaloader import Instaloader, Profile
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

# Инициализация Instaloader
loader = Instaloader()

# Аутентификация (если нужно)
loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

# Сбор постов по хэштегу
def fetch_instagram_posts(hashtag, count=10):
    posts = loader.get_hashtag_posts(hashtag)
    return [post.caption for post in posts[:count]]