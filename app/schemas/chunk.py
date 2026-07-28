from pydantic import BaseModel


class ChunkMetadata(BaseModel):

    chunk_id: str

    document_id: int

    document_name: str

    page_number: int

    chunk_index: int

    section_title: str

    start_offset: int

    end_offset: int

    token_count: int

    created_at: str


class Chunk(BaseModel):

    text: str

    metadata: ChunkMetadata