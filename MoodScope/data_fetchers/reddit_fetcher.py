import praw
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Сбор
def fetch_reddit_posts(query, count=10):
    posts = reddit.subreddit('all').search(query, limit=count)
    return [post.title for post in posts]
