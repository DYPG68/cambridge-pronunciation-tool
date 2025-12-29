# Cambridge Dictionary Pronunciation Tool

A lightweight, real-time web application built with Python and Streamlit to help English learners retrieve accurate **IPA (International Phonetic Alphabet)** transcriptions and audio pronunciations directly from the Cambridge Dictionary.

---

## 🚀 Features

* **Dual Dialect Support:** View both UK (British) and US (American) IPA transcriptions side-by-side.
* **Native Audio Streaming:** High-quality `.mp3` audio files streamed directly from Cambridge Dictionary servers.
* **Precision Scraping:** Utilizes targeted CSS selectors to avoid "secondary word" noise (e.g., ensuring you get the pronunciation for "suit" rather than a related idiom).
* **Minimalist UI:** Clean, responsive interface optimized for quick lookups.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend Logic:** [Python 3.x](https://www.python.org/)
* **Web Scraping:** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) & [Requests](https://requests.readthedocs.io/)
* **Data Parsing:** HTML/CSS Selector logic (DOM traversing)

---

## 🚀 Live Demo
Try the app right now! No installation needed.

🔗 **Live Version:** [https://cambridge-pronunciation-tool-bsquuadxwt5ew7zdr776bt.streamlit.app](https://cambridge-pronunciation-tool-bsquuadxwt5ew7zdr776bt.streamlit.app)

(Hosted for free on Streamlit Community Cloud)

---

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DYPG68/cambridge-pronunciation-tool.git
    cd cambridge-pronunciation-tool
    ```
2.  **(Recommended) Create and activate a virtual environment:**
    ```bash
    py -m venv venv
    venv\Scripts\activate    # Windows
    source venv/bin/activate  # Mac/Linux
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Alternatively: pip install streamlit beautifulsoup4 requests)
3.  **Launch the app:**
    ```bash
    streamlit run app.py
    ```
    Your browser will automatically open to a local host
---

## 🔍 How It Works

This tool solves a common web-scraping challenge: **Data Disambiguation**. 

Instead of scraping all text from the dictionary page, the script specifically targets the `.pos-header` class. This ensures that the IPA retrieved belongs strictly to the main headword, preventing the tool from picking up phonetic symbols of related phrases or sidebar suggestions. It filters for `audio/mpeg` sources to ensure cross-browser audio compatibility.

---

## 📄 License
Distributed under the MIT License. See [LICENSE](https://github.com/DYPG68/cambridge-pronunciation-tool/blob/main/LICENSE) for details.
