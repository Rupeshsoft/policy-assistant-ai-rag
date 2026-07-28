from app.services.document_reader import DocumentReader


class TextExtractor:

    @staticmethod
    def extract_document(file_path: str):

        extracted = DocumentReader.extract(file_path)

        result = []

        for item in extracted:

            result.append(
                {
                    "source": file_path,
                    "page": item.get("page", 1),
                    "text": item["text"]
                }
            )

        return result