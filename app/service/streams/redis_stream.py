import json
from redis.exceptions import ResponseError

class RedisStream:
    def __init__(self, redis):
        self.redis = redis

    async def ensure_group(self, key: str, group: str, start_id: str = "$"):
        try:
            await self.redis.xgroup_create(key, group, id=start_id, mkstream=True)
        except ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    async def xadd_json(self, key: str, body: dict):
        return await self.redis.xadd(key, {"event": json.dumps(body, ensure_ascii=False)})

    async def read_new(self, group: str, consumer: str, key: str, *, count=10, block=5000):
        return await self.redis.xreadgroup(group, consumer, streams={key: ">"}, count=count, block=block)

    async def ack_many(self, group: str, pairs: list[tuple[str, str]]):
        async with self.redis.pipeline(transaction=True) as pipe:
            for stream_name, msg_id in pairs:
                pipe.xack(stream_name, group, msg_id)
            await pipe.execute()