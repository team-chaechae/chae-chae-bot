import asyncio
import json
import logging
from app.rag.splitters import load_pdf_from_bytes, split_docs
from app.service.outbox_service import OutboxService
from app.service.streams.redis_stream import RedisStream

log = logging.getLogger("indexer")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class StreamIndexer:
    def __init__(self, outbox_service: OutboxService, stream: RedisStream, s3, vectorstore):
        self.outbox_service = outbox_service
        self.stream = stream
        self.s3 = s3
        self.vectorstore = vectorstore

    async def publish_pending_events(self, stream_key: str, limit: int) -> int:
        events = await self.outbox_service.claim_pending(limit)

        event_id_list = []
        for e in events:
            body = {**e.payload, "event_id": e.id}
            await self.stream.xadd_json(stream_key, body)
            event_id_list.append(e.id)
        
        if event_id_list:
            await self.outbox_service.mark_sent(event_id_list)

        return len(event_id_list)

    async def consume_events(
        self, stream_key: str, group: str, consumer: str, start_id: str = "0-0"
    ):
        await self.stream.ensure_group(stream_key, group, start_id=start_id)

        while True:
            msgs = await self.stream.read_new(group, consumer, stream_key)
            if not msgs:
                continue

            to_ack: list[tuple[str, str]] = []
            
            for stream_name, entries in msgs:
                for msg_id, fields in entries:
                    try:
                        payload = json.loads(fields["event"])
                        bucket = payload["bucket"]
                        object_key = payload["object_key"]
                        event_id = payload["event_id"]

                        # 1) S3 → 로드
                        docs = load_pdf_from_bytes(self.s3, bucket, object_key)

                        # 2) 문서 청킹
                        chunks = split_docs(docs)

                        # 3) 벡터스토어 인덱싱
                        self.vectorstore.add_documents(chunks)
                        if hasattr(self.vectorstore, "persist"):
                            self.vectorstore.persist()
                        
                        # 4) 완료 마킹
                        await self.outbox_service.mark_complete(event_id)

                        # 5) 성공시 ACK
                        to_ack.append((stream_name, msg_id))

                    except asyncio.CancelledError:
                        raise

                    except Exception:
                        log.exception("consume failed: msg_id=%s", msg_id)
                        continue
            
            if to_ack:
                await self.stream.ack_many(group, to_ack)