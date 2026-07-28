import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="policy_documents"
)


class ChromaService:

    @staticmethod
    def save_chunk(chunk):

        collection.add(

            ids=[
                chunk["metadata"]["chunk_id"]
            ],

            documents=[
                chunk["text"]
            ],

            embeddings=[
                chunk["embedding"]
            ],

            metadatas=[
                chunk["metadata"]
            ]

        )