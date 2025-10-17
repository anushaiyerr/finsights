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
        """
        Uploads a file to Gemini and retrieves structured, well-formatted insights.
        """
        try:
            uploaded_file = self.client.files.upload(file=file_path)

            prompt = (
                "You are a financial analyst with deep understanding of economics and healthcare finance. "
                "Carefully read the uploaded document and produce a professional, structured summary. "
                "Your output should follow this format:\n\n"
                "### 📘 Overview\n"
                "- A brief summary of what the document is about.\n\n"
                "### 💰 Financial Insights\n"
                "- Key quantitative or money-related points (revenues, costs, trends, etc.)\n\n"
                "### 🩺 Healthcare/Other Insights\n"
                "- Any sector-specific observations.\n\n"
                "### 🧭 Key Takeaways\n"
                "- 3–5 concise, actionable takeaways.\n\n"
                "Make it visually clear and easy to read. Use emojis, bold headers, and markdown for structure."
            )

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[uploaded_file, prompt]
            )

            return response.text.strip() if hasattr(response, "text") else "⚠️ No text in response."
        except Exception as e:
            return f"❌ Error analyzing file: {e}"
