from typing import List
from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str

    top_k: int = 5


class SourceDocument(BaseModel):

    chunk_id: str

    document_name: str

    page_number: int

    section_title: str

    chunk_text: str


class ChatResponse(BaseModel):

    question: str

    answer: str

    sources: List[SourceDocument]