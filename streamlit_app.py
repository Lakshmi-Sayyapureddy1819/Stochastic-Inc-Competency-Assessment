import streamlit as st
from src.ingestion import extract_text_from_pdf
from src.query_interface import ask_document_qa_agent
from src.arxiv_integration import search_arxiv

def main():
    st.set_page_config(page_title="Document Q&A AI Agent", page_icon="🤖", layout="wide")

    st.title("Document Q&A AI Agent with Gemini API")

    if "document_text" not in st.session_state:
        st.session_state.document_text = None

    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    if uploaded_file:
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner("Extracting text from PDF..."):
            st.session_state.document_text = extract_text_from_pdf("temp_uploaded.pdf")
        st.success("PDF text extracted successfully!")

    if st.session_state.document_text:
        with st.expander("Show extracted document text (optional)"):
            st.text_area("Document Text", st.session_state.document_text, height=300, disabled=True)

        user_query = st.text_input("Ask a question about the document:")
        if st.button("Get Answer") and user_query.strip():
            with st.spinner("Generating answer with Gemini AI..."):
                answer = ask_document_qa_agent(st.session_state.document_text, user_query)
            st.markdown("### Answer:")
            st.write(answer)

    st.markdown("---")

    st.header("Search Research Papers on Arxiv")
    arxiv_query = st.text_input("Enter keywords for Arxiv paper search:", key="arxiv_query")
    if st.button("Search Arxiv Papers"):
        if arxiv_query.strip():
            with st.spinner("Searching Arxiv..."):
                papers = search_arxiv(arxiv_query)
            if papers:
                for paper in papers:
                    st.markdown(f"**Title:** {paper['title']}")
                    st.markdown(f"**Summary:** {paper['summary']}")
                    st.markdown(f"[Read Paper]({paper['link']})")
                    st.markdown("---")
            else:
                st.info("No papers found for this query.")

if __name__ == "__main__":
    main()
