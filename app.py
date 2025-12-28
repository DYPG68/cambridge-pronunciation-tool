import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.title("🇬🇧 Cambridge Dictionary Pronunciation Tool")
st.markdown("Enter an English word to get UK/US 音标 (IPA) and listen to pronunciation audio!")

word = st.text_input("Enter a word:", placeholder="e.g., hello, beautiful")

if st.button("Search") or word:
    if not word.strip():
        st.warning("Please enter a word!")
    else:
        with st.spinner("Searching Cambridge Dictionary..."):
            time.sleep(0.5)  # delay
            
            url = f"https://dictionary.cambridge.org/dictionary/english/{word.lower().strip()}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code != 200 or "No results found" in response.text:
                    st.error("Word not found or spelling error. Try again!")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    uk_ipa = "Not found"
                    us_ipa = "Not found"
                    uk_audio_url = None
                    us_audio_url = None
                    
                    # Find all pronunciation blocks
                    for block in soup.find_all('div', class_='di-body'):
                        # Look for UK
                        uk_block = block.find('span', class_='uk')
                        if uk_block:
                            ipa = uk_block.find_next('span', class_='ipa')
                            if ipa:
                                uk_ipa = ipa.get_text(strip=True)
                            audio_source = block.find('source', src=lambda x: x and 'uk_pron' in x)
                            if audio_source:
                                uk_audio_url = "https://dictionary.cambridge.org" + audio_source['src']
                        
                        # Look for US
                        us_block = block.find('span', class_='us')
                        if us_block:
                            ipa = us_block.find_next('span', class_='ipa')
                            if ipa:
                                us_ipa = ipa.get_text(strip=True)
                            audio_source = block.find('source', src=lambda x: x and 'us_pron' in x)
                            if audio_source:
                                us_audio_url = "https://dictionary.cambridge.org" + audio_source['src']
                    
                    st.success(f"Found: **{word.capitalize()}**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🇬🇧 UK English")
                        st.markdown(f"**音標 (IPA):** /{uk_ipa}/")
                        if uk_audio_url:
                            st.audio(uk_audio_url)
                        else:
                            st.info("UK audio not available")
                    
                    with col2:
                        st.subheader("🇺🇸 US English")
                        st.markdown(f"**音標 (IPA):** /{us_ipa}/")
                        if us_audio_url:
                            st.audio(us_audio_url)
                        else:
                            st.info("US audio not available")
                            
            except Exception as e:
                st.error("Connection error. Check your internet or try later.")

st.markdown("---")
st.caption("Personal use only | Data from Cambridge Dictionary")