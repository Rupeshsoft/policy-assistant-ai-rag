from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database.database import Base


class ChunkMetadata(Base):

    __tablename__ = "chunk_metadata"

    id = Column(Integer, primary_key=True)

    chunk_id = Column(String(100), unique=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    document_name = Column(String(255))

    page_number = Column(Integer)

    chunk_index = Column(Integer)

    section_title = Column(String(255))

    start_offset = Column(Integer)

    end_offset = Column(Integer)

    token_count = Column(Integer)

    chunk_text = Column(Text)

    embedding_model = Column(String(100))

    chroma_id = Column(String(100))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )