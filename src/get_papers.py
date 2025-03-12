import requests
import csv
import argparse
import re
from typing import List, Dict, Any

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_papers(query: str) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(paper_ids: List[str]) -> Dict[str, Any]:
    if not paper_ids:
        return {}
    
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json"
    }
    response = requests.get(DETAILS_API_URL, params=params)
    response.raise_for_status()
    data = response.json().get("result", {})
    
    return data  # ✅ Return as a dictionary

def extract_affiliations(details: Dict[str, Any]) -> List[Dict[str, Any]]:
    extracted_data = []
    
    for uid in details.keys():
        if uid == "uids":
            continue  # ✅ Skip the "uids" key, which is just a list of IDs
        
        paper_info = details[uid]

        extracted_data.append({
            "PubmedID": uid,
            "Title": paper_info.get("title", "N/A"),
            "Publication Date": paper_info.get("pubdate", "N/A"),
        })
    
    return extracted_data

def save_to_csv(data: List[Dict[str, Any]], filename: str):
    if not data:
        print("No data to save.")
        return
    
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Query for searching research papers.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results.")
    args = parser.parse_args()

    paper_ids = fetch_papers(args.query)
    
    if args.debug:
        print(f"🔹 Paper IDs: {paper_ids}")

    details = fetch_paper_details(paper_ids)
    
    if args.debug:
        print(f"🔹 Paper Details: {details}")

    extracted_data = extract_affiliations(details)

    if args.debug:
        print(f"🔹 Extracted Data: {extracted_data}")

    if args.file:
        save_to_csv(extracted_data, args.file)
    else:
        print(extracted_data)

if __name__ == "__main__":
    main()
