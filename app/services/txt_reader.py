from typing import List, Dict


class TXTReader:

    @staticmethod
    def extract(file_path: str) -> List[Dict]:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            text = file.read()

        return [
            {
                "page": 1,
                "text": text
            }
        ]