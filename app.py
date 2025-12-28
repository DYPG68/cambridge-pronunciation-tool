import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.title("🇬🇧 Cambridge Dictionary Pronunciation Tool")
st.markdown("Enter an English word to get accurate UK/US 音标 (IPA) and audio!")

word = st.text_input("Enter a word:", placeholder="e.g., cloakroom, fraternize, hello")

if st.button("Search") or word:
    if not word.strip():
        st.warning("Please enter a word!")
    else:
        with st.spinner("Fetching from Cambridge Dictionary..."):
            time.sleep(1)  # Be polite to the server
            
            url = f"https://dictionary.cambridge.org/dictionary/english/{word.lower().strip()}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    st.error("Word not found or connection issue.")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    uk_ipas = []
                    us_ipas = []
                    uk_audio_url = None
                    us_audio_url = None
                    
                    # Find pronunciation entries
                    for entry in soup.find_all('div', class_='entry-body__el'):
                        # UK
                        uk_span = entry.find('span', class_='uk')
                        if uk_span:
                            ipa_spans = uk_span.find_next_siblings('span', class_='ipa')
                            uk_ipas = [f"/{ipa.get_text(strip=True)}/" for ipa in ipa_spans]
                            # Audio (look in the pron block)
                            audio = entry.find('amp-audio') or entry.find('audio')
                            if audio:
                                src = audio.get('src') or (audio.find('source') or {}).get('src')
                                if src and 'uk_pron' in src:
                                    uk_audio_url = "https://dictionary.cambridge.org" + src
                        
                        # US
                        us_span = entry.find('span', class_='us')
                        if us_span:
                            ipa_spans = us_span.find_next_siblings('span', class_='ipa')
                            us_ipas = [f"/{ipa.get_text(strip=True)}/" for ipa in ipa_spans]
                            audio = entry.find('amp-audio') or entry.find('audio')
                            if audio:
                                src = audio.get('src') or (audio.find('source') or {}).get('src')
                                if src and 'us_pron' in src:
                                    us_audio_url = "https://dictionary.cambridge.org" + src
                    
                    if not uk_ipas and not us_ipas:
                        st.error("No pronunciation found. Try a different word.")
                    else:
                        st.success(f"**{word.capitalize()}**")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🇬🇧 UK English")
                            if uk_ipas:
                                st.markdown("**音标 (IPA):** " + "  or  ".join(uk_ipas))
                            else:
                                st.info("UK not available")
                            if uk_audio_url:
                                st.audio(uk_audio_url)
                        
                        with col2:
                            st.subheader("🇺🇸 US English")
                            if us_ipas:
                                st.markdown("**音标 (IPA):** " + "  or  ".join(us_ipas))
                            else:
                                st.info("US not available")
                            if us_audio_url:
                                st.audio(us_audio_url)
                                
            except Exception:
                st.error("Connection failed. Check internet.")

st.caption("Built for English learners ❤️ | Data from Cambridge Dictionary | Personal use")
