from starlette.types import ASGIApp, Scope, Receive, Send
from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import async_scoped_session


class AsyncSessionMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    @inject
    def _get_session(
        self,
        session: async_scoped_session = Provide["infra.session"],
    ):
        return session  
        
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session = self._get_session()
        try:
            await self.app(scope, receive, send)
        finally:
            await session.remove()
