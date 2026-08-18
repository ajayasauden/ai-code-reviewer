import os 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google  import genai
from google.genai.errors import  APIError

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY missing from environment variables")

# initialize gemini and fastapi app
client = genai.Client(api_key = api_key)
app = FastAPI(
    title= "AI Code reviewer API",
    description="A FasrAPI backend that analyzes python code using google gemini",
    version="1.0.0"
)

# define request payload schema using pydantic
class CodeReviewRequest(BaseModel):
    code : str
    filename : str = "snippet.py"

# define api endpoints
@app.get("/")
def root():
    return {"message": "AI Code Reviewer api is running!"}   
  
@app.post("/api/review")
def review_code_endpoint(payload: CodeReviewRequest):
    if not payload.code.strip():
        raise HTTPException(status_code=400, detail="Code content cannot be empty")
    
    prompt = f"""
    You are a senior software engineer conducting a code review.
        Review the following Python code and provide feedback structured as follows:

        1. **Summary**: Brief description of what the code does.
        2. **Potential Bugs & Edge Cases**: Point out potential runtime errors or logical flaws.
        3. **Optimization & Style**: Suggest improvements (PEP 8, performance, readability).
        4. **Score**: Rate the code quality from 1 to 10 with a short justification.

        Code to review:
        ```python
        {payload.code}
        ```
        """

    try:
        response  = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt  

        )
        return {
            "filename": payload.filename,
            "status": "success",
            "review": response.text
        }
    except APIError as e :
        raise HTTPException(status_code=502, detail=f"Gemini API Error: {str(e)}")
    except Exception as e :
        raise HTTPException(status_code=500, detail= f"Internal Server Error: {str(e)}")