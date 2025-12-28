import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="Cambridge Pronunciation Tool", page_icon="🇬🇧")

st.title("🇬🇧 Cambridge Dictionary Pronunciation Tool")
st.markdown("Enter an English word to get UK/US IPA and listen to audio.")

word = st.text_input("Enter a word:", placeholder="e.g., suit, cloakroom")

if st.button("Search") or (word and len(word.strip()) > 0):
    word_clean = word.lower().strip()
    if not word_clean:
        st.warning("Please enter a word!")
    else:
        with st.spinner(f"Searching for '{word_clean}'..."):
            # Added a slight delay for stability
            time.sleep(0.3) 
            
            url = f"https://dictionary.cambridge.org/dictionary/english/{word_clean}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code != 200:
                    st.error("Could not connect to the dictionary. Please try again later.")
                elif "No results found" in response.text or "/spellcheck/" in response.url:
                    st.error("Word not found. Please check your spelling.")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Target the first main headword block to avoid unrelated words
                    # 'pos-header' contains the word, type, and IPA
                    header = soup.find('div', class_='pos-header')
                    
                    if not header:
                        st.error("Could not parse the pronunciation for this word.")
                    else:
                        uk_ipa = "N/A"
                        us_ipa = "N/A"
                        uk_audio = None
                        us_audio = None

                        # --- UK Extraction ---
                        uk_container = header.find('span', class_='uk')
                        if uk_container:
                            ipa_span = uk_container.find('span', class_='ipa')
                            if ipa_span:
                                uk_ipa = ipa_span.get_text(strip=True)
                            
                            # Find MP3 source specifically
                            audio_src = uk_container.find('source', type='audio/mpeg')
                            if audio_src and audio_src.get('src'):
                                uk_audio = "https://dictionary.cambridge.org" + audio_src['src']

                        # --- US Extraction ---
                        us_container = header.find('span', class_='us')
                        if us_container:
                            ipa_span = us_container.find('span', class_='ipa')
                            if ipa_span:
                                us_ipa = ipa_span.get_text(strip=True)
                            
                            audio_src = us_container.find('source', type='audio/mpeg')
                            if audio_src and audio_src.get('src'):
                                us_audio = "https://dictionary.cambridge.org" + audio_src['src']

                        st.success(f"Results for: **{word_clean}**")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🇬🇧 UK English")
                            st.info(f"/{uk_ipa}/")
                            if uk_audio:
                                st.audio(uk_audio)
                            else:
                                st.write("Audio unavailable")
                        
                        with col2:
                            st.subheader("🇺🇸 US English")
                            st.info(f"/{us_ipa}/")
                            if us_audio:
                                st.audio(us_audio)
                            else:
                                st.write("Audio unavailable")

            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Data source: Cambridge University Press & Assessment")
