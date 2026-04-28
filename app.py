import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd

# 1. Page Config (How it looks on a phone)
st.set_page_config(page_title="Chevy's Dutch Translator", page_icon="🇳🇱")
st.title('Chevy's Dutch Translator')
st.write("Translate instantly between English and Dutch!")

# 2. Load your local words (Optional, but keeps your custom list alive)
@st.cache_data
def get_local_data():
    try:
        # We use pandas to read the CSV easily for the web
        df = pd.read_csv('dutch_translation.csv')
        return dict(zip(df['english'], df['dutch']))
    except:
        return {}

local_words = get_local_data()

# 3. Sidebar for Settings
mode = st.sidebar.radio("Translation Direction", ["English to Dutch", "Dutch to English"])

# 4. The Translator Interface
word = st.text_input("Type your word here:").lower().strip()

if word:
    result = None
    
   # Check local list first
    if mode == "English to Dutch":
        # .strip() removes hidden spaces
        result = local_words.get(word)
    else:
        # Improved Dutch -> English search
        for eng, dut in local_words.items():
            if str(dut).strip().lower() == word:
                result = eng
                break

    if result:
        st.success(f"Local Match: {result}")
    else:
        # Use API if not in local list
        try:
            if mode == "English to Dutch":
                translated = GoogleTranslator(source='en', target='nl').translate(word)
            else:
                translated = GoogleTranslator(source='nl', target='en').translate(word)
            st.info(f"API Result: {translated}")
        except Exception as e:
            st.error("Could not connect to translation service.")

st.divider()
st.caption("Created for Alfred University Computer Science Project")
