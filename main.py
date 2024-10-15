from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure the genai API key
try:
    genai.configure(api_key=os.environ["API_KEY"])
except KeyError:
    raise HTTPException(status_code=500, detail="API_KEY not found in environment variables")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error configuring genai: {str(e)}")

class UserInput(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/generate")
async def generate_content(user_input: UserInput):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input.prompt)
        return {"response": response.text}
    except genai.GenerativeModelError as e:
        raise HTTPException(status_code=500, detail=f"Generative model error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")