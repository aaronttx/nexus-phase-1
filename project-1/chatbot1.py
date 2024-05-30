"""
IMPORTING LIBRARIES
"""

import json
from difflib import get_close_matches

"""HELPER FUNCTIONS FOR MANIPULATING KNOWLEDGE BASE"""

def load_kb(filepath: str) -> dict:
    with open(filepath, 'r') as fp:
        data: dict = json.load(fp)
    return data

def save_kb(filepath: str, data: dict):
    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent = 2)

"""INITIALIZING PATH FOR KNOWLEDGE BASE"""

# Path to the knowledge base
PATH = 'kb.json'
kb = load_kb(PATH)

"""FUNCTIONS FOR SEARCHING IN KB"""

def find_best_match(userqn: str, questions: list[str]):
    matches: list = get_close_matches(userqn, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer(question: str, knowledge_base: dict):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

"""MAIN CHATBOT LOOP"""

def chatbot():
    kb: dict = load_kb(PATH)
    print('Bot: Hello! I am a basic AI Chatbot!')
    while True:
        user_input: str = input('You: ')
        if user_input.lower() == 'quit':
            print('Bot: Goodbye!')
            break
        bestmatch: str|None = find_best_match(user_input, [q["question"] for q in kb["questions"]])

        if bestmatch:
            answer: str = get_answer(bestmatch, kb)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')
            if new_answer.lower() != 'skip':
                kb["questions"] .append({"question": user_input, "answer": new_answer})
                save_kb(str(PATH), kb)
                print('Bot: Thank you! I learned a new response!')

if __name__ == "__main__":
    chatbot()
