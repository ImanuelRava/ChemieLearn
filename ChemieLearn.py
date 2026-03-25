import streamlit as st
import time
import os
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="ChemieLearn",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Welcome Screen ---
st.title("Welcome to ChemieLearn 👋")
st.markdown("### Your hub for Chemistry Education")
st.markdown("Please select a section from the sidebar to begin.")

st.info("👉 **Quick Start:** Select **Chemistry Lecture** from the sidebar to view course materials.")

with st.spinner("Loading..."):
    time.sleep(1)

# --- AUDIO AUTO-PLAY FUNCTION ---
def play_audio_autoplay(file_path):
    # 1. Check if file exists
    if not os.path.exists(file_path):
        st.sidebar.error(f"Audio file missing: {file_path}")
        return

    # 2. Read file and convert to Base64
    try:
        audio_file = open(file_path, 'rb')
        audio_bytes = audio_file.read()
        b64 = base64.b64encode(audio_bytes).decode()
        
        # 3. Create HTML with autoplay and loop
        # Note: Browsers often block autoplay until user interacts with the page (clicking/tapping).
        html_string = f"""
            <audio autoplay loop>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                // Attempt to play via JavaScript (helps bypass some restrictions)
                var audio = document.getElementsByTagName('audio')[0];
                audio.volume = 0.5; // Set volume to 50%
            </script>
        """
        
        # 4. Render HTML
        st.components.v1.html(html_string, height=0)
        
    except Exception as e:
        st.sidebar.error(f"Error loading audio: {e}")

# --- SIDEBAR: AUDIO SECTION ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎵 Settings")

audio_path = "background.mp3" 

# This attempts to auto-play the music
play_audio_autoplay(audio_path)

# We also add a manual player just in case the browser blocks the auto-play
if os.path.exists(audio_path):
    st.sidebar.markdown("**Click Play if music doesn't start:**")
    st.sidebar.audio(open(audio_path, 'rb').read(), format="audio/mp3")
else:
    st.sidebar.warning("Add `background.mp3` to project folder.")