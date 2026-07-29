import json
import re
from typing import Any, List

# Try importing Ollama; fallback to a mock for testing
try:
    import ollama
    import httpx
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    httpx = None


class LLMService:

    # ---------- config ----------
    OLLAMA_MODEL = "llama3.2"  # or "mistral", "phi3", etc.

    # ---------- public interface ----------

    @staticmethod
    def generate_answer(question: str, chunks: list) -> str:
        """
        Top-level method: builds prompt, calls LLM, validates & formats.
        """
        prompt = LLMService.build_prompt(question, chunks)
        raw_response = LLMService.call_llm(prompt)
        validated = LLMService.validate_response(raw_response)
        final_answer = LLMService.format_answer(validated)
        return final_answer

    @staticmethod
    def build_prompt(question: str, chunks: list) -> str:
        """
        Build a structured prompt from the question and retrieved chunks.
        """
        context_parts = []

        for i, chunk in enumerate(chunks, 1):
            doc_name = chunk.get("document_name", "Unknown")
            page = chunk.get("page_number", "N/A")
            section = chunk.get("section_title", "N/A")
            text = chunk.get("chunk_text", "")

            context_parts.append(
                f"[{i}] Document : {doc_name}\n"
                f"    Page     : {page}\n"
                f"    Section  : {section}\n"
                f"    Content  :\n{text}\n"
            )

        context = "\n---\n".join(context_parts)

        prompt = (
            "You are an HR Policy Assistant.\n"
            "Answer ONLY from the provided context below.\n"
            "If the answer is not available in the context, say "
            '"I couldn\'t find this information."\n\n'
            "Context:\n"
            f"{context}\n\n"
            f"Question:\n{question}\n"
        )
        return prompt

    # ---------- internal helpers ----------

    @staticmethod
    def call_llm(prompt: str) -> str:
        """
        Send the prompt to Ollama and return the raw response string.
        Falls back to a simple mock if Ollama is not installed.
        """
        if OLLAMA_AVAILABLE:
            try:
                response = ollama.chat(
                    model=LLMService.OLLAMA_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response["message"]["content"]
            except (ollama.ResponseError, httpx.ConnectError, ConnectionError, ConnectionRefusedError) as exc:
                # Ollama binary/server not running or not reachable — graceful fallback
                return LLMService._mock_response(prompt)
            except Exception as exc:
                return f"[Ollama error: {exc}]"

    @staticmethod
    def validate_response(raw_response: str) -> str:
        """
        Clean and validate the raw LLM response.
        """
        if not raw_response or not raw_response.strip():
            return "I couldn't find this information."

        # Remove excessive whitespace / line breaks
        cleaned = re.sub(r"\n{3,}", "\n\n", raw_response.strip())

        # Strip common hallucination prefixes
        cleaned = re.sub(
            r"^(Based (on|upon) (the |)provided (context|information)|"
            r"According to the (context|document|text)|"
            r"As per the (context|document|text))[:,.]?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        ).strip()

        return cleaned

    @staticmethod
    def format_answer(validated_response: str) -> str:
        """
        Final formatting of the answer.
        """
        if not validated_response:
            return "I couldn't find this information."

        # Capitalise first letter
        answer = validated_response[0].upper() + validated_response[1:]

        # Ensure it ends with a full stop
        if answer[-1] not in ".!?":
            answer += "."

        return answer

    # ---------- fallback helpers ----------

    @staticmethod
    def _mock_response(prompt: str) -> str:
        """
        Simple fallback that extracts a plausible answer from the context part
        of the prompt when Ollama is not available.
        """
        # Try to grab the first chunk's content as a mock answer
        match = re.search(r"Content\s*:\n(.+?)(?:\n---|\Z)", prompt, re.DOTALL)
        if match:
            text = match.group(1).strip()[:300]
            return (
                f"Based on the policy documents, here is what I found:\n\n{text}\n\n"
                "For more details, please refer to the full document."
            )
        return "I couldn't find this information."
