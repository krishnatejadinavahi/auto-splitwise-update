from googleapiclient.discovery import build
import redis


class SplitwiseRedisUtils:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379)

    def store_group_id_for_user(self, group_id, current_user_id):
        self.client.set(f"sw-${current_user_id}", group_id)

