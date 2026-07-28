from app.services.embedding_service import EmbeddingService

from app.services.chroma_service import ChromaService

from app.services.mysql_service import save_chunk_metadata


class ChunkStorageService:

    @staticmethod
    def store_chunks(db, chunks):

        for chunk in chunks:

            embedding = EmbeddingService.generate_embedding(

                chunk["text"]

            )

            chunk["embedding"] = embedding

            ChromaService.save_chunk(chunk)

            save_chunk_metadata(db, chunk)