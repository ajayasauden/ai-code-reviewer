import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from google import genai
from google.genai.errors import APIError

# load api key from env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error : API_KEY not found in environment variables")
    sys.exit(1)

# Initialize gemini client    
client = genai.Client(api_key = api_key)  

def save_report_to_markdown(source_file_path,report_text):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok = True)

    # generating filename using source file and datetime

    base_name = os.path.splitext(os.path.basename(source_file_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"{base_name}_review_{timestamp}.md"
    file_path = os.path.join(output_dir, report_filename)

    # formatting report contents
    markdown_content = f"""# Code review report for `{os.path.basename(source_file_path)}`  
**Generated on :** {datetime.now().strftime("%Y%m%d %H%M%S")}
**Source file path :** `{source_file_path}`

----

    {report_text}
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    return file_path    


# read file from local and sends to gemini for review
def review_code(file_path):
    if not os.path.exists(file_path):
        print(f" Error : File '{file_path}' does not exists")
        return

    with open(file_path, "r" , encoding = "utf-8") as f:
        code_content = f.read()
        

    prompt = f"""
    You are a senior software engineer conducting a code review.
        Review the following Python code and provide feedback structured as follows:

        1. **Summary**: Brief description of what the code does.
        2. **Potential Bugs & Edge Cases**: Point out potential runtime errors or logical flaws.
        3. **Optimization & Style**: Suggest improvements (PEP 8, performance, readability).
        4. **Score**: Rate the code quality from 1 to 10 with a short justification.

        Code to review:
        {code_content}
        """
    print(f"Analyzing '{file_path}' using Gemini API..")
    try:
        response = client.models.generate_content(
            model = "gemini-3.6-flash",
            contents = prompt
        )

        report = response.text

        print("\n" + "="*50)
        print("code review report")
        print("\n" + "="*50)
        print(report)

        # Save to markdown file
        saved_path = save_report_to_markdown(file_path, report)
        print("\n"+"-"*50)
        print(f"Report successfully saved to {saved_path}")
        print("-"*50)


    except APIError as e :
       print(f"API request failed: {e}")
    except Exception as e :
       print(f"An unexpected error occured {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Python reviewer.py")
    else:
        target_file = sys.argv[1]       
        review_code(target_file)

       