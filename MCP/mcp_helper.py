import requests
import logging
import os

# -------------------------------------------
# Configuration
# -------------------------------------------

# You can set this in an environment variable if needed:
# Example: export BACKEND_URL=http://localhost:5000/api
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000/api")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# -------------------------------------------
# Helper Functions
# -------------------------------------------

def get_flashcards():
    """
    Fetch all flashcards from the backend API.
    Returns:
        list of flashcards (dict)
    """
    try:
        url = f"{BACKEND_URL}/flashcards"
        logger.info(f"Requesting flashcards from {url}")
        response = requests.get(url, timeout=5)

        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully retrieved {len(data)} flashcards.")
        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Network or backend error while fetching flashcards: {e}")
        return {"error": f"Failed to connect to backend at {BACKEND_URL}", "details": str(e)}

    except ValueError:
        logger.error("Failed to parse JSON from backend.")
        return {"error": "Invalid JSON response from backend."}


def add_flashcard(question, answer, topic=""):
    """
    Add a new flashcard to the backend API.
    Args:
        question (str): Flashcard question text.
        answer (str): Flashcard answer text.
        topic (str): Optional topic/category.
    Returns:
        dict: Result from backend or error message.
    """
    try:
        url = f"{BACKEND_URL}/flashcards"
        payload = {
            "question": question,
            "answer": answer,
            "topic": topic
        }

        logger.info(f"Sending new flashcard to {url}: {payload}")
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()

        data = response.json()
        logger.info("Successfully added flashcard.")
        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Network or backend error while adding flashcard: {e}")
        return {"error": f"Failed to connect to backend at {BACKEND_URL}", "details": str(e)}

    except ValueError:
        logger.error("Failed to parse backend response.")
        return {"error": "Invalid JSON response from backend."}
