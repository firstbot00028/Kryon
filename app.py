from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:

        if not GROQ_API_KEY:
            return jsonify({
                "reply": "GROQ_API_KEY not found"
            }), 500

        data = request.get_json()

        prompt = data.get("message", "").strip()

        if not prompt:
            return jsonify({
                "reply": "Empty message"
            }), 400

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": """
You are Zynora, a modern AI assistant created by Anandhakrishnan.

Be friendly, natural and helpful.
Match user's language.
Keep replies clean and conversational.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply
        })

    except requests.exceptions.RequestException as e:

        return jsonify({
            "reply": f"Groq Error: {str(e)}"
        }), 500

    except Exception as e:

        return jsonify({
            "reply": f"Server Error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000))
    )
