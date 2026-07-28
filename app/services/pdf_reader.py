import fitz
from typing import List, Dict


class PDFReader:

    @staticmethod
    def extract(file_path: str) -> List[Dict]:
        """
        Returns page-wise extracted text.

        Example:
        [
            {
                "page":1,
                "text":"...."
            }
        ]
        """

        pages = []

        pdf = fitz.open(file_path)

        try:

            for page_number, page in enumerate(pdf, start=1):

                text = page.get_text("text")

                pages.append(
                    {
                        "page": page_number,
                        "text": text.strip()
                    }
                )

        finally:
            pdf.close()

        return pages