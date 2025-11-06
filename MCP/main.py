import requests

# Test getting flashcards from MCP
res = requests.post("http://localhost:4000/tools/get_flashcards")
print(res.json())

# Test adding a new one
payload = {"question": "What is SQL?", "answer": "Structured Query Language", "topic": "Databases"}
res = requests.post("http://localhost:4000/tools/add_flashcard", json=payload)
print(res.json())