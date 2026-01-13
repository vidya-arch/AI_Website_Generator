from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebsiteRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_website(data: WebsiteRequest):
    system_prompt = """
    You are a professional web developer.
    Generate a responsive website.

    Return output strictly in this format:

    ---HTML---
    (HTML code)

    ---CSS---
    (CSS code)

    ---JS---
    (JavaScript code)
    """

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        system_prompt + "\nUser Request:\n" + data.prompt
    )

    return {"result": response.text}
