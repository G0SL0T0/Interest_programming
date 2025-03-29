from instaloader import Instaloader, Profile
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

loader = Instaloader()

loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

def fetch_instagram_posts(hashtag, count=10):
    posts = loader.get_hashtag_posts(hashtag)
    return [post.caption for post in posts[:count]]
