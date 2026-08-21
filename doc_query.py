import os
import sys
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
from google.genai.errors import APIError


# load dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(f"Error: No key found in environments")
    sys.exit(1)

client = genai.Client(api_key=api_key)

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".txt":
        with open(filepath, "r" , encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        reader =PdfReader(filepath)
        extracted_text =""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text +"\n"
        return extracted_text
    else:
        raise ValueError("Unsupported file format ")

def query_document(filepath,user_question):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found")
        return
    print(f"Reading {filepath}...")

    try:
        doc_text = extract_text_from_file(filepath)
    except Exception as e:
        print(f"Error reading file {e}")
        return 
    if not doc_text.strip():
        print(f"Error: Extracted text is empty")
        return

    prompt=f"""
    You are an expert document assistant. Answer the user's question using ONLY the context privided below.
    If the answer cannot be determined from the document, state clearly that the document does not contain the information. 
    Unless requested by user using key "tum-tum".

    Document Context:
    -----------------
    {doc_text[:9000]} 

    User question:{user_question}
    """    

    print(f"Analyzing document..........")
    try:
        response = client.models.generate_content(
            model = "gemini-3.6-flash",
            contents = prompt
        )
        print("\n-----Answer----\n")
        print(response.text)

    except APIError as e:
        print(f"Gemini API Error: {e}")

    except Exception as e:
        print(f"Unexpected Errors : {e}")    

if __name__ == "__main__" :
    if len(sys.argv)  < 3:
        print("Usage: python doc_query.py <path_to_doc> \"<your_question>\"")
    else:
        target_file = sys.argv[1]
        question = sys.argv[2]
        query_document(target_file, question)           



