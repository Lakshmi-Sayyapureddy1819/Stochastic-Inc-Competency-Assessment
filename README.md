# Stochastic-Inc-Competency-Assessment

# Document Q&A Chatbot with Gemini API and Arxiv Paper Search

This project is a Streamlit web application that enables users to:

- Upload PDF documents and ask multiple natural language questions about their content using the Google Gemini AI API (Document Q&A Chatbot).
- Search research papers on Arxiv via keyword queries with concise paper listing.

The app features a clean conversational chat UI, smooth user experience, and a visually appealing background.

---

## Features

- Upload and extract text from PDFs for in-depth AI-assisted Q&A.  
- Conversational interface with chat bubbles showing questions and AI-generated answers.  
- Seamless multi-question support without re-uploading PDFs.  
- Arxiv paper search with keyword input, presenting titles, summaries, and direct links.  
- Separate interfaces for Document Q&A and Arxiv search accessible via sidebar navigation.  
- Custom background image and styling for an engaging user experience.  

---

## Technology Stack

- **Frontend & Backend:** Streamlit (Python)  
- **AI Model:** Google Gemini API via `google-generativeai` Python client  
- **PDF Text Extraction:** `pdfplumber` (or your chosen method)  
- **Paper Search:** HTTP requests to Arxiv API  
- **Styling:** Embedded CSS with background images and responsive layout  

---

## Setup Instructions

### Prerequisites

- Python 3.8 or above  
- Google Gemini API key (saved in your `src/config.py` as `GOOGLE_API_KEY`)  
- Streamlit version 1.22+ for native chat UI support

### Install Dependencies

