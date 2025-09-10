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

```
pip install -r requirements.txt
```

*Example `requirements.txt` content:*

```
streamlit>=1.22
google-generativeai
pdfplumber
requests
python-dotenv
```

### Run the app locally

```
streamlit run streamlit_app.py
```

---

## Project Structure

```
project_root/
│
├── streamlit_app.py            # Main Streamlit app entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation file
├── background.jpg              # Background image (optional if local image used)
├── src/
│   ├── ingestion.py            # PDF text extraction logic
│   ├── query_interface.py      # Gemini API query function
│   ├── arxiv_integration.py    # Arxiv paper search functions
│   └── config.py               # API Key and config variables
└── ...
```

---

## Usage

### Document Q&A Chatbot

1. Upload a PDF document via the sidebar in the “Document Q&A Chatbot” page.  
2. Wait for text extraction confirmation.  
3. Ask any number of questions related to the document using the chat input box.  
4. View previous questions and AI answers as chat bubbles in the conversation area.

### Arxiv Paper Search

1. Switch to the “Arxiv Paper Search” page via sidebar navigation.  
2. Enter your desired keywords related to research topics.  
3. Click “Search Papers” to get a list of relevant research papers with title, brief summary, and links.

---

## Customization

- Change the background image by updating the URL or local file path in `inject_css()` function in `streamlit_app.py`.  
- Adjust UI colors and fonts via embedded CSS in the same function.  
- Update the Gemini model version or parameters inside `src/query_interface.py`.

---

## Troubleshooting

- Ensure your Google Gemini API key is correctly set in `src/config.py`.  
- Make sure Streamlit version is updated to **1.22 or newer** for chat functionality.  
- If you face import errors like `ModuleNotFoundError`, verify all dependencies are installed via `pip install -r requirements.txt`.  
- Monitor console logs for detailed error traces during API calls.

---

## Acknowledgments

- [Google Gemini API](https://developers.generativeai.google/) for powerful conversational AI.  
- [arXiv.org](https://arxiv.org/help/api) for accessible research paper data.  
- Unsplash for beautiful background images (https://unsplash.com).

---

For any questions or further support, please contact the developer.

