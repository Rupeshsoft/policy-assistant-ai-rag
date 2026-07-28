from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.chat import ChatRequest

from app.services.semantic_search import SemanticSearchService
from app.services.llm_service import LLMService

router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)


@router.post("/search")
def search_chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    results = SemanticSearchService.search(
        request.question,
        request.top_k
    )

    documents = results["documents"][0]

    metadata = results["metadatas"][0]

    retrieved_chunks = []

    for doc, meta in zip(documents, metadata):

        retrieved_chunks.append(
            {
                "chunk_id": meta["chunk_id"],

                "document_name": meta["document_name"],

                "page_number": meta["page_number"],

                "section_title": meta["section_title"],

                "chunk_text": doc
            }
        )

    answer = LLMService.generate_answer(
        request.question,
        retrieved_chunks
    )

    return {

        "question": request.question,

        "answer": answer,

        "sources": retrieved_chunks
    }
