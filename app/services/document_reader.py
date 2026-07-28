import os
import fitz                     # PyMuPDF
from docx import Document
from app.services.pdf_reader import PDFReader
from app.services.docx_reader import DOCXReader
from app.services.txt_reader import TXTReader

class DocumentReader:
    
    @staticmethod
    def extract(file_path: str):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return PDFReader.extract(file_path)

        elif extension == ".docx":
            return DOCXReader.extract(file_path)

        elif extension == ".txt":
            return TXTReader.extract(file_path)

        else:
            raise Exception(
                f"Unsupported File Type : {extension}"
            )
            
            

    @staticmethod
    def read_document(file_path: str) -> str:
        """
        Detect file type and return extracted text.
        """

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return DocumentReader.read_pdf(file_path)

        elif extension == ".docx":
            return DocumentReader.read_docx(file_path)

        elif extension == ".txt":
            return DocumentReader.read_txt(file_path)

        else:
            raise Exception(f"Unsupported file type : {extension}")

    # --------------------------------------------------

    @staticmethod
    def read_pdf(file_path: str):

        document = fitz.open(file_path)

        pages = []

        for page_no, page in enumerate(document, start=1):

            pages.append({
                "page": page_no,
                "text": page.get_text("text")
            })

        document.close()

        return pages


    # @staticmethod
    # def read_pdf(file_path: str) -> str:
    #     """
    #     Extract text from PDF using PyMuPDF
    #     """

    #     document = fitz.open(file_path)

    #     extracted_text = []

    #     for page in document:

    #         text = page.get_text("text")

    #         extracted_text.append(text)

    #     document.close()

    #     return "\n".join(extracted_text)

    # --------------------------------------------------

    @staticmethod
    def read_docx(file_path: str) -> str:
        """
        Extract text from DOCX
        """

        doc = Document(file_path)

        paragraphs = []

        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        return "\n".join(paragraphs)

    # --------------------------------------------------

    @staticmethod
    def read_txt(file_path: str) -> str:
        """
        Read TXT file
        """

        with open(file_path, "r", encoding="utf-8") as file:

            return file.read()