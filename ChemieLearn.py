import streamlit as st
import time

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

# Auto-redirect logic (optional visual cue)
with st.spinner("Loading..."):
    time.sleep(1)