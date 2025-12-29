Cambridge Dictionary Pronunciation Tool
A Python-based web application that retrieves real-time International Phonetic Alphabet (IPA) transcriptions and high-quality audio pronunciations from the Cambridge Dictionary.

🚀 Features
Dual Pronunciation: Provides both UK and US IPA transcriptions.

Native Audio: Streams .mp3 pronunciation files directly from Cambridge's servers.

Targeted Scraping: Uses refined CSS selectors to ensure accurate data extraction for specific headwords.

Responsive UI: Built with Streamlit for a clean, interactive user experience.

🛠️ Tech Stack
Language: Python

Interface: Streamlit

Scraping: BeautifulSoup4, Requests

Parsing: HTML/CSS Selector logic

📦 Installation
Clone the repository:

Bash

git clone https://github.com/yourusername/cambridge-pronunciation-tool.git
Install dependencies:

Bash

pip install streamlit beautifulsoup4 requests
Run the app:

Bash

streamlit run app.py
