from flask import Flask, render_template, request
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")


if not openai.api_key:
    raise RuntimeError("Error: OpenAI API key not configured. Check your .env file or Heroku config.")


app = Flask(__name__)

def generate_email_response(input_text):
    """
    Generates a response email based on the provided email content and instructions.
    """
    if not openai.api_key:
        return "Error: OpenAI API key not configured. Check your environment variables."
    
    messages = [
        {
            "role": "system",
            "content": "You are a professional email writer. Generate only email responses based on the provided email content and instructions. Do not add unrelated information.",
        },
        {"role": "user", "content": input_text},
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating email: {e}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        if len(input_text.split()) > 500:
            return render_template("index.html", error="Input cannot exceed 500 words.", response_email=None)
        response_email = generate_email_response(input_text)
        return render_template("index.html", error=None, response_email=response_email)

    return render_template("index.html", error=None, response_email=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the port from Heroku or default to 5000
    app.run(debug=False, host="0.0.0.0", port=port)
