import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY in .env file")
        self.client = genai.Client(api_key=api_key)

    def analyze_file(self, file_path: str):
        """Uploads a file and gets analysis directly from Gemini."""
        try:
            # ✅ Upload file directly (no mime_type args)
            uploaded_file = self.client.files.upload(file=file_path)

            # ✅ Simple prompt
            prompt = (
                "Analyze this document and summarize key financial and healthcare insights. "
                "Give clear bullet points grouped by topic."
            )

            # ✅ Pass uploaded file directly to Gemini
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[uploaded_file, prompt]
            )

            return response.text.strip() if hasattr(response, "text") else "No text in response."
        except Exception as e:
            return f"❌ Error analyzing file: {e}"
