from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from sqlalchemy import text

from app.api.v1 import dataset_router, rag_router
from app.containers.main import MainContainer
from app.core.fastapi.middleware import AsyncSessionMiddleware
from app.database.session import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="채채봇",
        description="채채봇 API 입니다.",
        version="1.0.0",
        lifespan=lifespan,
    )

    container = MainContainer()
    app.container = container

    app.add_middleware(AsyncSessionMiddleware)          
    app.include_router(dataset_router.router)
    app.include_router(rag_router.router)              

    
    @app.get("/health", status_code=status.HTTP_200_OK, summary="Health check")
    async def health_check(request: Request):
        infra = request.app.container.infra()

        db = infra.session()
        try:
            await db.execute(text("SELECT 1"))
            return {"status": "ok", "db": "ok"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"status": "fail", "db": "fail", "error": str(e)},
            )
        finally:
            await db.close()
            

    return app


app = create_app()