from flask import Flask, jsonify
app = Flask(__name__)
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

@app.get("/")
def index():
    return jsonify({"message": "Hello World!"}), 200

if __name__ == "__main__":
    app.run()