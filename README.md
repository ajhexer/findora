# Findora Search Engine

## Overview
Findora is a search engine tailored to the contents of Persian news websites. This project was developed as the final project for the Information Retrieval course. It ranks search results using the tf-idf scoring method.

## Features
- **Search Functionality**: Allows users to search through Persian news articles.
- **Ranking Mechanism**: Implements tf-idf scoring for ranking search results.
- **Preprocessing**: Includes preprocessing steps for handling Persian text data.
- **Utilities**: Various utility functions to support the main functionalities.

## Project Structure
- **preprocess/**: Directory containing preprocessing scripts.
- **utils/**: Directory containing utility scripts.
- **engine/**: Core search engine implementation.
  - `query.py`: Handles query processing.
  - `index.py`: Manages the indexing of documents.
  - `search_engine.py`: Main search engine logic.
  - `utils.py`: Utility functions used by the engine.
- **main.py**: Entry point for running the search engine.
- **downloads/**: Directory for storing downloaded news articles.
- **test.ipynb**: Jupyter Notebook for testing and demonstration purposes.



