from docx import Document
from typing import List, Dict


class DOCXReader:

    @staticmethod
    def extract(file_path: str) -> List[Dict]:

        document = Document(file_path)

        paragraphs = []

        paragraph_number = 1

        for para in document.paragraphs:

            text = para.text.strip()

            if text:

                paragraphs.append(
                    {
                        "paragraph": paragraph_number,
                        "text": text
                    }
                )

                paragraph_number += 1

        return paragraphs