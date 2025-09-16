import asyncio
import logging
import signal
import json

from app.containers.main import MainContainer

log = logging.getLogger("publisher")

async def run_publisher(batch: int = 100, poll_interval: float = 3) -> None:
    container = MainContainer()
    infra = container.infra()
    domains = container.domains()

    stream_indexer = domains.stream_indexer()
    stream = infra.stream_name()

    stop = asyncio.Event()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, stop.set)
    loop.add_signal_handler(signal.SIGINT, stop.set)

    try:
        while not stop.is_set():
            try:
                published = await stream_indexer.publish_pending_events(stream, batch)
                if not published:
                    await asyncio.sleep(poll_interval)
            except Exception:
                log.exception("publish loop error")
                await asyncio.sleep(min(5.0, poll_interval * 4))
    finally:
        redis = infra.redis()
        if hasattr(redis, "aclose"):
            await redis.aclose()

if __name__ == "__main__":
    asyncio.run(run_publisher())