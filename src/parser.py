import pdfplumber
import requests
import json
import re

class LocalAIParser:
    def __init__(self, model_name="llama3.2:1b"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def extract_text(self, pdf_path):
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Page 1 usually has the header info (Account No, Name, Bank)
                if len(pdf.pages) > 0:
                    text += pdf.pages[0].extract_text() or ""
                # Grab Page 2 if Page 1 is too short (less than 100 chars)
                if len(text) < 100 and len(pdf.pages) > 1:
                    text += pdf.pages[1].extract_text() or ""
        except Exception as e:
            return ""
        return text

    def parse(self, pdf_path):
        raw_text = self.extract_text(pdf_path)
        
        if not raw_text.strip():
            return {"error": "Empty text. File might be an image."}

        prompt = f"""
        You are a strict data extraction engine. Analyze the text below and extract 5 facts.
        
        INSTRUCTIONS:
        1. Find the "Issuer" (Bank Name) at the very top of the document.
        2. Find the "Account Number".
        3. Find the "Statement Date".
        4. Find the "Total Balance".
        
        RETURN ONLY JSON with these keys:
        - "issuer": The exact name of the bank or provider as written in the text.
        - "account_last_4": The last 4 digits of the account number.
        - "statement_date": Date in YYYY-MM-DD.
        - "due_date": Date in YYYY-MM-DD (or null).
        - "total_balance": Numeric value (e.g. 1234.50).

        TEXT TO ANALYZE:
        {raw_text[:2500]}
        """

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.1, 
                "seed": 42
            }
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            data = json.loads(result['response'])
            
            
            # 1. Clean up Issuer
            issuer = data.get('issuer', 'Unknown')
            if issuer and issuer not in raw_text:
                # If the AI guessed a name not in the text, mark it as suspicious
                if "Bank" not in issuer and "Card" not in issuer: 
                     data['issuer'] = "Not Found in Text (AI Guess)"
            
            return data

        except Exception as e:
            return {"error": str(e), "details": "Model failed to return JSON"}