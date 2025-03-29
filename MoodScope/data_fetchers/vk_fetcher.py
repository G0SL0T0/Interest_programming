import vk_api
from config import VK_ACCESS_TOKEN

vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
vk = vk_session.get_api()

def fetch_vk_posts(query, count=10):
    posts = vk.wall.search(q=query, count=count)
    return [post['text'] for post in posts['items']]
