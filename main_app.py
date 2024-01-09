import os

from dotenv import load_dotenv

from src.views import app

load_dotenv()

os.environ.get("OPENAI_API_KEY")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)