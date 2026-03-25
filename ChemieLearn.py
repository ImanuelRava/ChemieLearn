import streamlit as st
import time
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="ChemieLearn",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Welcome Screen ---
st.title("Welcome to ChemieLearn 👋")
st.markdown("### Your hub for Chemistry Education")
st.markdown("Please select a section from the sidebar to begin.")

st.info("👉 **Quick Start:** Select **Chemistry Lecture** from the sidebar to view course materials.")

# Auto-redirect logic (optional visual cue)
with st.spinner("Loading..."):
    time.sleep(1)

# --- SIDEBAR: AUDIO PLAYER ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎵 Background Music")

# Check if file exists to prevent crash
music_file = "background.mp3"
if os.path.exists(music_file):
    # Open the file and read bytes
    audio_file = open(music_file, 'rb')
    audio_bytes = audio_file.read()
    
    # Display the audio player
    st.sidebar.audio(audio_bytes, format='audio/mp3')
else:
    st.sidebar.warning("Add `background.mp3` to enable music.")