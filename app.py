import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.title("🇬🇧 Cambridge Dictionary Pronunciation Tool")
st.markdown("Enter an English word for accurate UK/US 音标 (IPA) and audio!")

word = st.text_input("Enter a word:", placeholder="e.g., suit, cloakroom, hello")

if st.button("Search") or word:
    if not word.strip():
        st.warning("Please enter a word!")
    else:
        with st.spinner("Fetching from Cambridge Dictionary..."):
            time.sleep(1)
            
            url = f"https://dictionary.cambridge.org/dictionary/english/{word.lower().strip()}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            
            try:
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code != 200:
                    st.error("Page not found. Check spelling!")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Find the first main entry body (most common meaning)
                    entry = soup.find('div', class_='entry-body__el')
                    if not entry:
                        st.error("No pronunciation found for this word.")
                    else:
                        uk_ipas = []
                        us_ipas = []
                        uk_audio = None
                        us_audio = None
                        
                        # UK pronunciation block
                        uk_block = entry.find('div', class_='pron dpron-i uk')
                        if uk_block:
                            ipa_spans = uk_block.find_all('span', class_='ipa')
                            uk_ipas = [f"/{ipa.get_text(strip=True)}/" for ipa in ipa_spans]
                            # Audio
                            audio_tag = uk_block.find_parent().find('audio') or uk_block.find_next('audio')
                            if audio_tag:
                                source = audio_tag.find('source', src=lambda s: s and 'uk_pron' in s)
                                if source:
                                    uk_audio = "https://dictionary.cambridge.org" + source['src']
                        
                        # US pronunciation block
                        us_block = entry.find('div', class_='pron dpron-i us')
                        if us_block:
                            ipa_spans = us_block.find_all('span', class_='ipa')
                            us_ipas = [f"/{ipa.get_text(strip=True)}/" for ipa in ipa_spans]
                            # Audio
                            audio_tag = us_block.find_parent().find('audio') or us_block.find_next('audio')
                            if audio_tag:
                                source = audio_tag.find('source', src=lambda s: s and 'us_pron' in s)
                                if source:
                                    us_audio = "https://dictionary.cambridge.org" + source['src']
                        
                        st.success(f"**{word.capitalize()}** (primary meaning)")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🇬🇧 UK English")
                            if uk_ipas:
                                st.markdown("**音標 (IPA):** " + "  |  ".join(uk_ipas))
                                if uk_audio:
                                    st.audio(uk_audio)
                            else:
                                st.info("No UK pronunciation")
                        
                        with col2:
                            st.subheader("🇺🇸 US English")
                            if us_ipas:
                                st.markdown("**音標 (IPA):** " + "  |  ".join(us_ipas))
                                if us_audio:
                                    st.audio(us_audio)
                            else:
                                st.info("No US pronunciation")
                                
            except Exception as e:
                st.error("Connection error. Try again later.")

st.caption("Uses primary meaning from Cambridge Dictionary")
