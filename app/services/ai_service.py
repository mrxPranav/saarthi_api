import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama3-8b-8192")
        self.client = AsyncGroq(api_key=self.api_key)

    async def generate_title(self, note_text: str) -> str:
        prompt = f"Generate a short, concise title (maximum 10 words) for the following note content. Return ONLY the title text, nothing else.\n\nNote Content:\n{note_text}"
        
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )
            return chat_completion.choices[0].message.content.strip().strip('"')
        except Exception as e:
            print(f"Error generating title with Groq: {e}")
            return "Untitled Note"
