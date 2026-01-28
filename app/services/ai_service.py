import os
import logging
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

# Configure logging to stdout for Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama3-8b-8192")
        self.client = AsyncGroq(api_key=self.api_key)

    async def generate_title(self, note_text: str) -> str:
        prompt = f"Generate a short, concise title (maximum 10 words) for the following note content. Return ONLY the title text, nothing else.\n\nNote Content:\n{note_text}"
        
        logger.info(f"AI Prompt: {prompt}")
        
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
            response = chat_completion.choices[0].message.content.strip().strip('"')
            logger.info(f"AI Response: {response}")
            return response
        except Exception as e:
            logger.error(f"Error generating title with Groq: {e}", exc_info=True)
            return "Untitled Note"
