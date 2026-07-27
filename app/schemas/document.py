from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):

    id: int

    filename: str

    original_filename: str

    filetype: str

    filesize: int

    status: str

    created_at: datetime

    class Config:

        from_attributes = True