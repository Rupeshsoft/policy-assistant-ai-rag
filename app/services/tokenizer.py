from transformers import AutoTokenizer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


class TokenizerService:

    @staticmethod
    def token_count(text: str):

        return len(
            tokenizer.encode(
                text,
                add_special_tokens=False
            )
        )

    @staticmethod
    def encode(text):

        return tokenizer.encode(
            text,
            add_special_tokens=False
        )

    @staticmethod
    def decode(tokens):

        return tokenizer.decode(
            tokens,
            skip_special_tokens=True
        )