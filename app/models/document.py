from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    original_filename = Column(String(255), nullable=False)

    filepath = Column(String(500), nullable=False)

    filetype = Column(String(20))

    filesize = Column(Integer)

    uploaded_by = Column(Integer, ForeignKey("users.id"))

    status = Column(String(20), default="UPLOADED")

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())