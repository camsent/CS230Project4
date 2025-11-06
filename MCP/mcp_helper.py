import requests

BACKEND_URL = "http://localhost:5000/api"

def get_flashcards():
    response = requests.get(f"{BACKEND_URL}/flashcards")
    return response.json()

def add_flashcard(question, answer, topic=""):
    payload = {"question": question, "answer": answer, "topic": topic}
    response = requests.post(f"{BACKEND_URL}/flashcards", json=payload)
    return response.json()