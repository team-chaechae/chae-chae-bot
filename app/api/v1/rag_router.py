from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, HTTPException
from langchain_core.runnables import Runnable
from app.schemas.rag import AskIn, AskOut


router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/ask", response_model=AskOut)
@inject
async def ask(
    body: AskIn, rag_chain: Runnable[str, str] = Depends(Provide["domains.rag_chain"])
):
    try:
        answer = await rag_chain.ainvoke(body.question)
        return AskOut(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
