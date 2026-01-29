import os
import logging
from groq import AsyncGroq
from dotenv import load_dotenv

# Load .env from the app directory (parent of services)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# Configure logging to stdout for Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.client = AsyncGroq(api_key=self.api_key)

    async def get_custom_completion(self, role: str, content: str) -> dict:
        logger.info(f"Custom AI Request - Role: {role}, Content: {content}")
        
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": role,
                        "content": content,
                    }
                ],
                model=self.model,
            )
            response = chat_completion.choices[0].message.content.strip()
            logger.info(f"Custom AI Response: {response}")
            return {"response": response, "model": self.model}
        except Exception as e:
            logger.error(f"Error getting custom completion with Groq: {e}", exc_info=True)
            raise e

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
