from src.ingestion import extract_text_from_pdf
from src.query_interface import ask_document_qa_agent
from src.arxiv_integration import search_arxiv

def main():
    print("Welcome to the Document Q&A AI Agent!")

    pdf_path = input("Enter path to PDF document: ")
    document_text = extract_text_from_pdf(pdf_path)

    while True:
        query = input("\nAsk a question about the document (or type 'arxiv' to search papers, 'quit' to exit): ").strip()
        if query.lower() == "quit":
            print("Goodbye!")
            break
        elif query.lower() == "arxiv":
            arxiv_query = input("Enter keywords to search Arxiv papers: ").strip()
            papers = search_arxiv(arxiv_query)
            for paper in papers:
                print(f"\nTitle: {paper['title']}\nSummary: {paper['summary']}\nLink: {paper['link']}\n")
        else:
            answer = ask_document_qa_agent(document_text, query)
            print(f"\nAnswer:\n{answer}")

if __name__ == "__main__":
    main()
