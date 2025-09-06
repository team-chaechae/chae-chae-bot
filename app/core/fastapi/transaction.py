from functools import wraps
from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import async_scoped_session

class transactional:
    def __init__(self, commit: bool = False):
        self.commit = commit

    @inject
    def _get_session(
        self,
        session: async_scoped_session = Provide["infra.session"],
    ):
        return session 

    def __call__(self, func):
        @wraps(func)
        async def _wrapped(*args, **kwargs):
            session = self._get_session()
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            else:
                if self.commit:
                    await session.commit()
            
            return result

        return _wrapped