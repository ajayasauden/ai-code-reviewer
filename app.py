import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# load environment variables
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found")
    st.stop()

client = genai.Client(api_key=api_key)

# configure streamlit page layout
st.set_page_config(
    page_title="AI Engineering Suite",
    page_icon="⚡",
    layout="wide"
)

st.title("AI Engineering Multi-Tool Suite")
st.markdown("Powered by **Google Gemini** and **Streamlit**")
st.markdown("----")

# creating navigating tabs
tab1,tab2 = st.tabs(["AI Code Reviewer", "CSV Data Summarizer"])

# tab1: code reviewer
with tab1:
    st.subheader("Automated python code reviewer")
    st.text("Paste your python code below")

    default_code = "def calculate_avg(numbers):\n   total=sum(numbers)\n    return total/len(numbers)"
    code_input = st.text_area("Python code snippet", default_code,height=150)

    if st.button("Run Code Review"):
        if not code_input.strip():
            st.warning("Please enter python code")

        else:
            with st.spinner("Analyzing code with Gemini...."):
                prompt=f"""
                You are a senior software engineer conducting a code review.
                Review the following Python code and structure your feedback as:
                1. **Summary**
                2. **Potential Bugs & Edge Cases**
                3. **Optimization & Style**
                4. **Score (1-10)**

                Code:
                ```python
                {code_input}
                ```
                """
                try:
                    response=client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )    
                    st.markdown("### Review report")
                    st.markdown(response.text)

                except APIError as e:
                    st.error(f"Gemini API Error: {e}")   

                except Exception as e :
                    st.error(f"Unexpectes error: {e}")     

with tab2:
    st.subheader("Dataset and CSV AI Summarizer")
    st.text("Upload a csv file")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        df= pd.read_csv(uploaded_file, encoding="utf-8")


        st.markdown("**Dataset Preview**")
        st.dataframe(df.head())

        if st.button("Generate Data Report"):
            with st.spinner("Processing dataset..."):
                stats={
                    "row_count":len(df),
                    "column_count":len(df.columns),
                    "columns":list(df.columns),
                    "missing_values":df.isnull().sum().to_dict(),
                    "numeric_summary":df.describe().to_dict() if not df.select_dtypes(include='number').empty else "No numeric columns"

                }

                prompt = f"""
                You are a Senior Data Analyst. Analyze these dataset statistics and prepare an executive summary report:
                - Total Rows: {stats['row_count']}
                - Total Columns: {stats['column_count']}
                - Columns: {stats['columns']}
                - Missing Values: {stats['missing_values']}
                - Statistics: {stats['numeric_summary']}

                Structure your response into:
                1. **Executive Overview**
                2. **Key Data Insights**
                3. **Business Recommendations**
                """

                try:
                    response=client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                    st.markdown("### Executive Report")
                    st.markdown(response.text)

                except APIError as e:
                    st.error(f"Gemini API Error: {e}")    


