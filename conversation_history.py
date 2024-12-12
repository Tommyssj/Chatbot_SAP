# conversation_history.py

conversation_history = []

def add_to_history(user_message, bot_reply):
    global conversation_history
    conversation_history.append(f"User: {user_message}")
    conversation_history.append(f"Assistant: {bot_reply}")

def get_history():
    return "\n".join(conversation_history)
