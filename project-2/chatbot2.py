"""INSTALL GRADIO USING 'pip install gradio' """

"""IMPORTING LIBRARIES"""

import json
from difflib import get_close_matches
import gradio as gr

"""HELPER FUNCTIONS FOR MANIPULATING KNOWLEDGE BASE"""

def load_kb(filepath: str) -> dict:
    with open(filepath, 'r') as fp:
        data: dict = json.load(fp)
    return data

def save_kb(filepath: str, data: dict):
    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent=2)

def update_kb(user_input: str, new_answer: str, kb: dict, kb_path: str):
    if new_answer.lower() != "skip":
        kb["questions"].append({"question": user_input, "answer": new_answer})
        save_kb(kb_path, kb)
        return "Thank you! I learned a new response!"
    else:
        return "No new response added."

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

"""MAIN CHATBOT FUNCTIONS"""

def chatbot(user_input: str, kb: dict):
    bestmatch = find_best_match(user_input, [q["question"] for q in kb["questions"]])
    if bestmatch:
        answer = get_answer(bestmatch, kb)
        return answer
    else:
        return "I don't know the answer. Can you teach me?"

# Function to handle chat interaction
def chat_interaction(user_input, chat_history):
    bot_response = chatbot(user_input, kb)
    chat_history.append((user_input, bot_response))
    if bot_response == "I don't know the answer. Can you teach me?":
        return chat_history, gr.update(visible=True), gr.update(interactive=True)
    else:
        return chat_history, gr.update(visible=False), gr.update(interactive=True)

# Function to handle teaching the bot
def teach_bot(user_input, new_answer, chat_history):
    teach_response = update_kb(user_input, new_answer, kb, PATH)
    chat_history[-1] = (chat_history[-1][0], teach_response)  # Update last bot response
    return chat_history, gr.update(visible=False), gr.update(interactive=True)

"""MAIN GUI LOOP"""

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# My Chatbot")

    initial_greeting = "Hello! How can I help you today?"
    chat_history = gr.State([(None, initial_greeting)])  # Initialize with a greeting message
    chat_log = gr.Chatbot(value=[(None, initial_greeting)])  # Set the initial value for the chat log
    user_input = gr.Textbox(show_label=False, placeholder="Type your question here...")
    new_answer = gr.Textbox(show_label=False, placeholder='Type the answer or "skip" to skip...', visible=False)

    def submit_interaction(user_input, chat_history):
        chat_history, new_answer_visible, user_input_interactive = chat_interaction(user_input, chat_history)
        return chat_history, new_answer_visible, user_input_interactive, ""

    def submit_teach(user_input, new_answer, chat_history):
        chat_history, new_answer_visible, user_input_interactive = teach_bot(user_input, new_answer, chat_history)
        return chat_history, new_answer_visible, user_input_interactive, ""

    user_input.submit(submit_interaction, inputs=[user_input, chat_history], outputs=[chat_log, new_answer, user_input])
    new_answer.submit(submit_teach, inputs=[user_input, new_answer, chat_history], outputs=[chat_log, new_answer, user_input])

demo.launch()
