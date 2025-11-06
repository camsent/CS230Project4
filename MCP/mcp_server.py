from flask import Flask, request, jsonify
import mcp_helper

app = Flask(__name__)

@app.route("/tools/get_flashcards", methods=["POST"])
def get_flashcards():
    flashcards = mcp_helper.get_flashcards()
    return jsonify(flashcards)

@app.route("/tools/add_flashcard", methods=["POST"])
def add_flashcard():
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")
    topic = data.get("topic", "")
    result = mcp_helper.add_flashcard(question, answer, topic)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=4000)
