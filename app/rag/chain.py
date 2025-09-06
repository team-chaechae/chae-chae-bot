from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama


PROMPT_TEMPLATE = """
Answer the question based only on the following context.
Do not use any external information or knowledge. 
If the answer is not in the context, answer "잘 모르겠습니다.".

[Context]
{context}

[Question] 
{question}

[Answer]
""".strip()

def _format_docs(docs: List[Document]) -> str:
    return "\n\n".join(d.page_content for d in docs)

def build_bm25_retriever(vectorstore: Chroma) -> BM25Retriever:
    col = vectorstore._collection  # 내부 핸들 (버전 따라 바뀔 수 있음)
    raw = col.get(include=["documents", "metadatas"])
    docs = [
        Document(page_content=txt, metadata=meta)
        for txt, meta in zip(raw.get("documents", []), raw.get("metadatas", []))
        if txt
    ]
    bm25 = BM25Retriever.from_documents(docs)
    return bm25

def build_ensemble_retriever(vectorstore: Chroma) -> EnsembleRetriever:
    chroma_threshold = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.6, "k": 2},
    )

    bm25 = build_bm25_retriever(vectorstore)

    return EnsembleRetriever(
        retrievers=[chroma_threshold, bm25],
        weights=[0.6, 0.4],
        search_kwargs={"k": 2},
    )

def build_rag_chain(vectorstore: Chroma, llm: ChatOllama):
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    retriever = build_ensemble_retriever(vectorstore)

    retriever_chain = retriever | RunnableLambda(_format_docs)

    chain = (
        {"context": retriever_chain, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain