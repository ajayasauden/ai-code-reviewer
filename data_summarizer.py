import os
import sys
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# 1. Load Environment & Initialize Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

def extract_dataset_stats(csv_path):
    """Reads a CSV file using Pandas and extracts basic descriptive statistics."""
    df = pd.read_csv(csv_path)
    
    stats = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_summary": df.describe().to_dict() if not df.select_dtypes(include='number').empty else "No numeric columns"
    }
    return stats

def generate_ai_data_report(csv_path):
    """Parses dataset stats and uses Gemini to generate a business summary."""
    if not os.path.exists(csv_path):
        print(f"Error: Dataset '{csv_path}' not found.")
        return

    print(f"Reading dataset '{csv_path}' with Pandas...")
    try:
        stats = extract_dataset_stats(csv_path)
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    prompt = f"""
    You are a Senior Data Analyst. Analyze the following dataset statistics and prepare an executive summary report.

    Dataset File: `{os.path.basename(csv_path)}`
    Total Rows: {stats['row_count']}
    Total Columns: {stats['column_count']}
    Columns: {stats['columns']}
    Missing Values: {stats['missing_values']}
    Statistical Overview: {stats['numeric_summary']}

    Please structure your response as follows:
    1. **Executive Overview**: High-level summary of what dataset contains.
    2. **Key Data Insights**: Highlight notable patterns, distributions, or missing data warnings.
    3. **Business Recommendations**: 2-3 strategic next steps based on the numbers.
    """

    print("Generating AI data analysis report...")
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        
        print("\n" + "=" * 50)
        print("DATA ANALYSIS REPORT")
        print("=" * 50 + "\n")
        print(response.text)

    except APIError as e:
        print(f"Gemini API Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python data_summarizer.py <path_to_csv_file>")
    else:
        target_csv = sys.argv[1]
        generate_ai_data_report(target_csv)