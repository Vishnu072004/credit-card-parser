import streamlit as st
import pandas as pd
import tempfile
import os
from src.parser import LocalAIParser

# Page Config
st.set_page_config(
    page_title="AI Statement Parser",
    page_icon="💳",
    layout="centered"
)


st.title("💳 AI Credit Card Statement Parser")
st.markdown("""
**Privacy-First Architecture**: This tool processes your documents using **Local Llama 3.2**. 
No data is uploaded to external clouds (OpenAI/Google).
""")

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    model = st.text_input("Local Model Name", value="llama3.2:1b")
    st.info(f"Using model: {model}")

# File Uploader
uploaded_files = st.file_uploader(
    "Upload Bank Statements (PDF)", 
    type="pdf", 
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Extract Data"):
        
        # Initialize Parser with the model from sidebar
        parser = LocalAIParser(model_name=model)
        results = []
        
        # Progress Bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, file in enumerate(uploaded_files):
            status_text.text(f"Processing {file.name}...")
            
            # Save to temp file (pdfplumber needs a path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.getvalue())
                tmp_path = tmp.name
            
            # Parse
            data = parser.parse(tmp_path)
            data["filename"] = file.name 
            results.append(data)
            
            # Cleanup
            os.remove(tmp_path)
            progress_bar.progress((idx + 1) / len(uploaded_files))

        status_text.text("Processing Complete!")
        
        # Display Results
        if results:
            df = pd.DataFrame(results)
            
            # Reorder columns 
            preferred_order = ["filename", "issuer", "total_balance", "due_date", "statement_date", "account_last_4"]
            cols = [c for c in preferred_order if c in df.columns] + [c for c in df.columns if c not in preferred_order]
            
            st.subheader("Extraction Results")
            st.dataframe(df[cols], use_container_width=True)

            # Download Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download as CSV",
                csv,
                "parsed_statements.csv",
                "text/csv",
                key='download-csv'
            )