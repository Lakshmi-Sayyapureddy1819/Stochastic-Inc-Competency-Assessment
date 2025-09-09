import requests
import xml.etree.ElementTree as ET
from src.config import ARXIV_API_URL

def search_arxiv(query, max_results=3):
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }
    response = requests.get(ARXIV_API_URL, params=params)
    root = ET.fromstring(response.content)
    results = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        link = entry.find("{http://www.w3.org/2005/Atom}id").text
        results.append({"title": title, "summary": summary, "link": link})
    return results
