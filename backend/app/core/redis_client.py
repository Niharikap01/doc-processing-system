import redis
import json

REDIS_URL = "redis://localhost:6379/0"

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True
)


def publish_event(channel: str, message: dict):
    redis_client.publish(channel, json.dumps(message))


def subscribe_channel(channel: str):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    return pubsub