import streamlit as st
from src.ingestion import extract_text_from_pdf
from src.query_interface import ask_document_qa_agent

def main():
    st.set_page_config(
        page_title="📄 Document Q&A Chatbot",
        page_icon="🤖",
        layout="centered"
    )

    st.title("📄 Document Q&A Chatbot with Gemini API")
    st.markdown("Upload a PDF document and ask multiple questions — answers appear as chat messages.")

    # Initialize session state
    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar for PDF upload and chat reset
    with st.sidebar:
        st.header("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.document_text = None

    # Handle PDF upload
    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            with open("temp_uploaded.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.document_text = extract_text_from_pdf("temp_uploaded.pdf")
            st.session_state.chat_history = []
        st.success("PDF loaded! You can now ask questions.")

    # Show extracted document text preview (optional)
    if st.session_state.document_text:
        with st.expander("📄 Preview Extracted Document Text"):
            st.text_area("Document Text", st.session_state.document_text, height=200, disabled=True)

        # Display chat messages
        for chat in st.session_state.chat_history:
            with st.chat_message(chat['role']):
                st.markdown(chat['message'])

        # Chat input box
        prompt = st.chat_input("Ask a question about the document")
        if prompt:
            # Append user message
            st.session_state.chat_history.append({"role": "user", "message": prompt})

            # Generate AI answer
            with st.spinner("Generating answer..."):
                answer = ask_document_qa_agent(st.session_state.document_text, prompt)

            # Append assistant message
            st.session_state.chat_history.append({"role": "assistant", "message": answer})

            # Rerun script to display new messages
            st.experimental_rerun()

    else:
        st.info("Please upload a PDF document to start chatting.")

if __name__ == "__main__":
    main()
