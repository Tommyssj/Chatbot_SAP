from flask import Flask, request, jsonify
import openai
from textblob import TextBlob
import re

# Initialize Flask app
app = Flask(__name__)

# Hardcode OpenAI API key
openai.api_key = ""
# In-memory conversation history
conversation_history = []

@app.route('/')
def home():
    return "Welcome to the Chat API! Use the /chat endpoint to communicate."

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    user_message = request.json.get('message', '')

    # Append user message to conversation history
    conversation_history.append(f"User: {user_message}")

    # Analyze sentiment
    sentiment = TextBlob(user_message).sentiment.polarity
    if sentiment < -0.5:
        tone = "empathetic"
    elif sentiment > 0.5:
        tone = "enthusiastic"
    else:
        tone = "neutral"

    # Handle specific intents
    if "weather" in user_message:
        return jsonify({"reply": "I can't fetch live weather updates yet, but you can ask me other questions!"})
    elif re.search(r'(\d+)\s*\+\s*(\d+)', user_message):
        numbers = re.findall(r'\d+', user_message)
        result = sum(map(int, numbers))
        return jsonify({"reply": f"The result of your calculation is: {result}"})

    # Default OpenAI API response
    try:
        prompt = "\n".join(conversation_history) + f"\nAssistant ({tone}):"
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        bot_reply = response.choices[0].text.strip()

        # Append bot reply to conversation history
        conversation_history.append(f"Assistant: {bot_reply}")

        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
