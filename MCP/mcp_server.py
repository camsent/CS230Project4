from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import mcp_helper

# -------------------------------------------
# Flask App Setup
# -------------------------------------------
app = Flask(__name__)
CORS(app)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# -------------------------------------------
# MCP Endpoints
# -------------------------------------------

@app.route("/tools/get_flashcards", methods=["POST"])
def get_flashcards_tool():
    """
    Fetch all flashcards from the backend.
    This endpoint is called by Claude via MCP.
    """
    logger.info("Received request: get_flashcards_tool")
    try:
        flashcards = mcp_helper.get_flashcards()
        logger.info(f"Fetched {len(flashcards)} flashcards from backend.")
        return jsonify(flashcards), 200
    except Exception as e:
        logger.error(f"Error fetching flashcards: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/tools/add_flashcard", methods=["POST"])
def add_flashcard_tool():
    """
    Add a new flashcard to the backend.
    Expected JSON: { "question": "...", "answer": "...", "topic": "..." }
    """
    logger.info("Received request: add_flashcard_tool")
    try:
        data = request.get_json()
        question = data.get("question")
        answer = data.get("answer")
        topic = data.get("topic", "")

        if not question or not answer:
            return jsonify({"error": "Missing 'question' or 'answer'"}), 400

        result = mcp_helper.add_flashcard(question, answer, topic)
        logger.info(f"Added flashcard: {question}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error adding flashcard: {e}")
        return jsonify({"error": str(e)}), 500


# -------------------------------------------
# Root Health Check
# -------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "MCP server running", "tools": ["get_flashcards", "add_flashcard"]})


# -------------------------------------------
# Run Server
# -------------------------------------------
if __name__ == "__main__":
    logger.info("Starting MCP server on http://localhost:4000 ...")
    app.run(port=4000)
