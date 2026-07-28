from app.models.chunk_metadata import ChunkMetadata


def save_chunk_metadata(db, chunk):

    metadata = chunk["metadata"]

    row = ChunkMetadata(

        chunk_id=metadata["chunk_id"],

        document_id=metadata["document_id"],

        document_name=metadata["document_name"],

        page_number=metadata["page_number"],

        chunk_index=metadata["chunk_index"],

        section_title=metadata["section_title"],

        start_offset=metadata["start_offset"],

        end_offset=metadata["end_offset"],

        token_count=metadata["token_count"],

        chunk_text=chunk["text"],

        embedding_model="all-MiniLM-L6-v2",

        chroma_id=metadata["chunk_id"]

    )

    db.add(row)

    db.commit()