from google import genai as Ai
from google.genai import types
from PIL import Image
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ai = Ai.Client(api_key=GEMINI_API_KEY)
model = "gemini-2.5-flash"


def artificial_intelligence(text=None, file=None):
    if file is not None:
        image_bytes = file.read()
        if text is None:
            text = "Describe the visual content of this image without any introductory phrases about it being a screenshot or a picture. Simply list what you see."
        response = ai.models.generate_content(model=model, contents=[types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'), f"{text}"])

        return response

    elif text is not None:
        response = ai.models.generate_content(model=model, config=Ai.types.GenerateContentConfig(system_instruction="Your name is Jakman Ai and you were created by an author named Dmytro. If they ask you what your name is -- answer: 'my name is Nuxus AI'. If they ask you who made you -- answer: 'I was created by Dmytro'. If they ask you when you were created, say you were created in 2026."), contents=text)

        return response.text
