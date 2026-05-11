import asyncio
import json

from app.core.redis_client import redis_client
from app.core.ws_manager import manager


class RedisListener:
    def __init__(self):
        self.pubsub = redis_client.pubsub()

        # subscribe to all document channels
        self.pubsub.psubscribe("document_*")

    async def start(self):
        loop = asyncio.get_event_loop()

        while True:
            message = await loop.run_in_executor(
                None,
                lambda: self.pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1
                )
            )

            if message:
                try:
                    data = json.loads(message["data"])

                    channel = message["channel"]

                    # document_1 -> 1
                    doc_id = int(channel.split("_")[1])

                   
                    await manager.broadcast(doc_id, data)

                except Exception as e:
                    print("Redis Listener Error:", e)

            await asyncio.sleep(0.1)


listener = RedisListener()