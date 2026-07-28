import re


class HeadingDetector:

    PATTERNS = [

        r"^[A-Z][A-Z ]+$",

        r"^\d+\.",

        r"^Chapter",

        r"^SECTION",

        r"^Policy",

        r"^Article"

    ]

    @staticmethod
    def is_heading(text):

        text = text.strip()

        for pattern in HeadingDetector.PATTERNS:

            if re.match(pattern, text):
                return True

        return False