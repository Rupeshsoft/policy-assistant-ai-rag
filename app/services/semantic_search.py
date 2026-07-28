from app.services.embedding_service import EmbeddingService
from app.services.chroma_service import collection


class SemanticSearchService:

    @staticmethod
    def search(question: str, top_k: int = 5):

        embedding = EmbeddingService.generate_embedding(question)

        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        return results