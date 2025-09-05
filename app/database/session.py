from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
)

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# 2) 비동기 엔진
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

# 3) 비동기 세션팩토리
AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)

# 요청(Task) 단위로 격리되는 세션 프록시
AsyncScopedSession = async_scoped_session(
    session_factory=AsyncSessionFactory,
    scopefunc=current_task,
)