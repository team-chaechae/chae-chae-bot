from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever


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

MULTI_QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""Generate three different versions of the given user question to retrieve relevant documents from a vector database. The goal is to reframe the question from various perspectives to overcome limitations of distance-based similarity search.

    The generated questions should have the following characteristics:
    1. Maintain the core intent of the original question but use different expressions or viewpoints.
    2. Include synonyms or related concepts where possible.
    3. Slightly broaden or narrow the scope of the question to potentially include diverse relevant information.

    Write each question on a new line and include only the questions.

    [Original question]
    {question}
    
    [Alternative questions]
    """,
)


class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> List[str]:
        """Split the text into lines and remove empty lines."""
        return [line.strip() for line in text.strip().split("\n") if line.strip()]


def build_chroma_retriever(
    vectorstore: Chroma, k: int = 5, score_threshold: float = 0.5
):
    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": score_threshold, "k": k},
    )


def build_multi_query_custom_retriever(vectorstore: Chroma, llm: ChatOllama):
    return MultiQueryRetriever(
        retriever=build_chroma_retriever(vectorstore),
        llm_chain=MULTI_QUERY_PROMPT | llm | LineListOutputParser(),
        parser_key="lines",
    )


def build_cross_encoder_rerank_retriever(
    vectorstore: Chroma, llm: ChatOllama, re_ranker: CrossEncoderReranker
):
    return ContextualCompressionRetriever(
        base_compressor=re_ranker,
        base_retriever=build_multi_query_custom_retriever(vectorstore, llm),
    )


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(d.page_content for d in docs)


def build_rag_chain(
    vectorstore: Chroma, llm: ChatOllama, re_ranker: CrossEncoderReranker
):
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    retriever = build_cross_encoder_rerank_retriever(vectorstore, llm, re_ranker)

    retriever_chain = retriever | RunnableLambda(format_docs)

    chain = (
        {"context": retriever_chain, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
