# 🔒 Privacy-First Credit Card Statement Parser

A robust, AI-powered tool that extracts key financial data from unstructured credit card statements (PDFs). 

Unlike traditional parsers that rely on brittle Regex rules or expensive cloud APIs, this project uses **Local Large Language Models (LLMs)** to process sensitive financial data entirely offline. No data ever leaves your machine.

---

## 🎯 Objective
To build a universal parser capable of handling heterogeneous statement layouts (e.g., Chase, HDFC, Amex) without:
1.  **Hardcoding rules** for every specific bank format.
2.  **Compromising privacy** by sending bank details to public APIs (OpenAI/Google).

## 🚀 Key Features
* **Privacy-Centric:** Built on [Ollama](https://ollama.com) running **Llama 3.2**. All inference happens on `localhost`.
* **Layout Agnostic:** Uses semantic understanding to find "Total Due" or "Account Number" regardless of where they are on the page.
* **Lightweight Architecture:** Optimized to run on standard laptops (requires <2GB RAM) using the `llama3.2:1b` model.
* **Hallucination Guards:** Includes post-processing logic to verify that extracted entities (like Bank Name) actually exist in the source text.
* **Structured Export:** Automatically normalizes unstructured text into clean CSV datasets.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **AI Engine:** [Ollama](https://ollama.com/) (running `llama3.2:1b`)
* **PDF Processing:** `pdfplumber` (Layout-preserving text extraction)
* **Language:** Python 3.10+

---

## ⚙️ Installation & Setup

### 1. Install Prerequisites
You need **Python** installed. You also need **Ollama** to run the AI model.

* Download Ollama: [ollama.com](https://ollama.com)
* Pull the lightweight model (Run this in your terminal):
    ```bash
    ollama pull llama3.2:1b
    ```

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/credit-card-parser.git](https://github.com/YOUR_USERNAME/credit-card-parser.git)
cd credit-card-parser
