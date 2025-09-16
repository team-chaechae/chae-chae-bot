import asyncio
import logging
import signal
import socket
from app.containers.main import MainContainer

log = logging.getLogger("consumer")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def run_consumer(start_id: str = "0-0") -> None:
    container = MainContainer()
    infra = container.infra()
    domains = container.domains()

    stream_indexer = domains.stream_indexer()
    stream = infra.stream_name()
    group = infra.consumer_group()

    base_consumer = infra.consumer_name()
    consumer = f"{base_consumer}-{socket.gethostname()}"

    stop = asyncio.Event()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, stop.set)
    loop.add_signal_handler(signal.SIGINT, stop.set)

    task = asyncio.create_task(
        stream_indexer.consume_events(
            stream_key=stream, group=group, consumer=consumer, start_id=start_id
        )
    )

    try:
        await stop.wait()
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        r = infra.redis()
        if hasattr(r, "aclose"):
            await r.aclose()

        log.info("consumer stopped")


if __name__ == "__main__":
    asyncio.run(run_consumer())
