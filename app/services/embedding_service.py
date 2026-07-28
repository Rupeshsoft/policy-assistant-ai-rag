from sentence_transformers import SentenceTransformer


class EmbeddingService:

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    @staticmethod
    def generate_embedding(text: str):

        embedding = EmbeddingService.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()