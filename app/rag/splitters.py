from typing import List
from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import fitz

EMB_MODEL = "BAAI/bge-m3"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 100

_tokenizer = AutoTokenizer.from_pretrained(EMB_MODEL)

import logging

logger = logging.getLogger(__name__)


def count_tokens(text: str) -> int:
    return len(_tokenizer.encode(text, add_special_tokens=False))


def make_text_splitter(chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer=_tokenizer,
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )


def split_docs(
    docs: List[Document], chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP, debug=False
):
    splitter = make_text_splitter(chunk_size, overlap)
    chunks = splitter.split_documents(docs)
    for i, c in enumerate(chunks):
        c.metadata = {
            **c.metadata,
            "chunk_index": i,
            "token_len": count_tokens(c.page_content),
        }
    if debug:
        total_tokens = sum(count_tokens(c.page_content) for c in chunks)
        logger.info("chunks=%d, tokens=%d", len(chunks), total_tokens)

    return chunks


def load_pdf_from_bytes(s3, bucket: str, key: str):
    obj = s3.get_object(Bucket=bucket, Key=key)
    raw = obj["Body"].read()

    pdf = fitz.open(stream=raw, filetype="pdf")
    docs = []
    for i, page in enumerate(pdf):
        text = page.get_text("text") or ""
        if text.strip():
            docs.append(
                Document(
                    page_content=text,
                    metadata={"page": i + 1, "source": f"s3://{bucket}/{key}"},
                )
            )
    return docs
