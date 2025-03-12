"# Project Readme" 
# PubMed Paper Fetcher

A CLI tool to fetch research papers from PubMed based on user queries.

## 🚀 Features
- Searches PubMed for research papers
- Filters results based on affiliations
- Saves results as a CSV file

## 📦 Installation

1. Install [Poetry](https://python-poetry.org/)
2. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd pubmed-paper-fetcher
   ```
3. Install dependencies:
   ```sh
   poetry install --no-root
   ```

## 🔧 Usage

Run the script with a query:

```sh
poetry run python src/get_papers.py "cancer research" --file results.csv
```

Enable debug mode:

```sh
poetry run python src/get_papers.py "cancer research" --debug
```

## 🛠 Dependencies
- Python 3.8+
- `requests` (for API calls)

## 📜 License
MIT License

