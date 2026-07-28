from datetime import datetime
import nltk

from app.services.tokenizer import TokenizerService
from app.services.heading_detector import HeadingDetector


class ChunkingService:

    @staticmethod
    def chunk_document(
        document_id,
        document_name,
        extracted_pages,
        chunk_size=300,
        overlap=50
    ):

        chunks = []

        chunk_index = 0

        current_heading = "General"

        for page in extracted_pages:

            page_no = page["page"]

            text = page["text"]

            sentences = nltk.sent_tokenize(text)

            current_chunk = ""

            start_offset = 0

            for sentence in sentences:

                if HeadingDetector.is_heading(sentence):

                    current_heading = sentence

                candidate = current_chunk + " " + sentence

                token_count = TokenizerService.token_count(candidate)

                if token_count <= chunk_size:

                    current_chunk = candidate.strip()

                else:

                    tokens = TokenizerService.encode(current_chunk)

                    overlap_tokens = tokens[-overlap:]

                    overlap_text = TokenizerService.decode(
                        overlap_tokens
                    )

                    chunk = {

                        "text": current_chunk,

                        "metadata": {

                            "chunk_id":

                            f"{document_id}_{page_no}_{chunk_index}",

                            "document_id": document_id,

                            "document_name": document_name,

                            "page_number": page_no,

                            "chunk_index": chunk_index,

                            "section_title": current_heading,

                            "start_offset": start_offset,

                            "end_offset":

                            start_offset + len(current_chunk),

                            "token_count":

                            TokenizerService.token_count(
                                current_chunk
                            ),

                            "created_at":

                            datetime.utcnow().isoformat()

                        }

                    }

                    chunks.append(chunk)

                    chunk_index += 1

                    start_offset += len(current_chunk)

                    current_chunk = overlap_text + " " + sentence

            if current_chunk.strip():

                chunk = {

                    "text": current_chunk,

                    "metadata": {

                        "chunk_id":

                        f"{document_id}_{page_no}_{chunk_index}",

                        "document_id": document_id,

                        "document_name": document_name,

                        "page_number": page_no,

                        "chunk_index": chunk_index,

                        "section_title": current_heading,

                        "start_offset": start_offset,

                        "end_offset":

                        start_offset + len(current_chunk),

                        "token_count":

                        TokenizerService.token_count(
                            current_chunk
                        ),

                        "created_at":

                        datetime.utcnow().isoformat()

                    }

                }

                chunks.append(chunk)

                chunk_index += 1

        return chunks