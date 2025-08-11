import streamlit as st
from textblob import TextBlob
import pandas as pd
import re
import unicodedata
import replicate
from deep_translator import GoogleTranslator

def translate_to_indonesian(text):
    try:
        translated = GoogleTranslator(source='auto', target='id').translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {e}"
        
api_token = st.secrets["REPLICATE_API_TOKEN"]

# Inisialisasi client dengan token
replicate_client = replicate.Client(api_token=api_token)

def generate_response(prompt):
    try:
        granite_prompt = (
            "You are a compassionate mental health support assistant. "
            "Always respond in Bahasa Indonesia and focus on providing empathetic, helpful advice "
            "related to mental health, stress, anxiety, depression, and wellbeing. "
            "Do NOT translate or explain words in English. "
            "Correct the letters in the word so that there are no missing or extra spaces."
            f"User input: {prompt}"
        )
        output = replicate.run(
            "ibm-granite/granite-3.3-8b-instruct",
            input={"prompt": granite_prompt}
        )
        if isinstance(output, list):
            text = ' '.join(s.strip() for s in output)
        else:
            text = output.strip()

        text = re.sub(r'\s+', ' ', text)  
        text = text.strip()
        return text

    except Exception as e:
        return f"Error saat memanggil model: {e}"
    
def clean_response(text):
    # Hapus teks dalam tanda kurung yang mengandung huruf Inggris
    text = re.sub(r'\([^()]*[a-zA-Z][^()]*\)', '', text)
    # Hapus hashtag (#...)
    text = re.sub(r'#\S+', '', text)
    # Hapus bagian 'Translation' dan seterusnya
    text = re.sub(r'Translation:.*', '', text, flags=re.DOTALL)
    # Bersihkan spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_whitespace(text):
    # Ganti semua whitespace unicode ke spasi biasa
    text = ''.join(' ' if unicodedata.category(c).startswith('Z') else c for c in text)
    return text

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", polarity
    elif 0.1 < polarity <= 0.5:
        return "Positive", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", polarity
    elif -0.5 < polarity < -0.1:
        return "Negative", polarity
    else:
        return "Very Negative", polarity

def provide_coping_strategy(sentiment):
    strategies = {
        "Very Positive": "Keep up the positive vibes! Consider sharing your good mood with others.",
        "Positive": "It's great to see you're feeling positive. Keep doing what you're doing!",
        "Neutral": "Feeling neutral is okay. Consider engaging in activities you enjoy.",
        "Negative": "It seems you're feeling down. Try to take a break and do something relaxing.",
        "Very Negative": "I'm sorry to hear that you're feeling very negative. Consider talking to a friend or seeking professional help."
    }
    return strategies.get(sentiment, "Keep going, you're doing great!")

def display_disclaimer():
    st.sidebar.markdown(
        "<h2 style='color: #FF5733;'>Data Privacy Disclaimer</h2>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<span style='color: #FF5733;'>This application stores your session data, including your messages and "
        "sentiment analysis results, in temporary storage during your session. "
        "This data is not stored permanently and is used solely to improve your interaction with the chatbot. "
        "Please avoid sharing personal or sensitive information during your conversation.</span>",
        unsafe_allow_html=True
    )

# --- CSS Styling Updated ---
st.markdown("""
<style>
.chat-message {
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 8px;
    max-width: 70%;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    line-height: 1.4;
    word-wrap: break-word;
    color: white;
}
.user-message {
    background-color: #000000;
    align-self: flex-end;
}
.bot-message {
    background-color: #222222;
    align-self: flex-start;
}
.user-container {
    display: flex;
    justify-content: flex-end;
}
.bot-container {
    display: flex;
    justify-content: flex-start;
}
#chat-input-container {
    position: fixed;
    bottom: 10px;
    left: 0;
    width: 100%;
    padding: 10px 20px;
    background-color: #f9f9f9;
    box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
    display: flex;
    gap: 10px;
    box-sizing: border-box;
    z-index: 1000;
}
#chat-input-container input[type="text"] {
    flex-grow: 1;
    padding: 10px;
    border-radius: 25px;
    border: 1px solid #ccc;
    font-size: 16px;
}
#chat-input-container button {
    background-color: #000000;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    font-weight: bold;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

st.title("Mental Health Support Chatbot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'mood_tracker' not in st.session_state:
    st.session_state['mood_tracker'] = []

# Display chat messages
chat_placeholder = st.empty()

def render_chat():
    with chat_placeholder.container():
        for sender, message in st.session_state['messages']:
            if sender == "You":
                st.markdown(f"""
                <div class="user-container">
                    <div class="chat-message user-message">{message}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-container">
                    <div class="chat-message bot-message">{message}</div>
                </div>
                """, unsafe_allow_html=True)

render_chat()

# Custom input area fixed at bottom using st.markdown and st.form hack
with st.form(key="chat_form", clear_on_submit=True):
    st.markdown('<div id="chat-input-container">', unsafe_allow_html=True)
    user_message = st.text_input("", key="input_text", placeholder="Ketik pesan kamu...")
    submit_button = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button and user_message:
    st.session_state['messages'].append(("You", user_message))

    sentiment, polarity = analyze_sentiment(user_message)
    coping_strategy = provide_coping_strategy(sentiment)

    response = generate_response(user_message)

    st.session_state['messages'].append(("Bot", response))
    st.session_state['mood_tracker'].append((user_message, sentiment, polarity))

    chat_placeholder.empty()
    render_chat()
st.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; 
                text-align: center; padding: 10px; 
                color: white; font-size: 14px;">
        Design by <a href="https://jackdev-portofolio.netlify.app/" target="_blank" style="color: #FF5733; text-decoration: none;">jackdev</a>
    </div>
    """,
    unsafe_allow_html=True
)
