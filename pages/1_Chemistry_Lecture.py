import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Chemistry Lecture - ChemieLearn", layout="wide", page_icon="favicon.ico")

# --- CSS Styling ---
st.markdown("""
<style>
    .course-item { padding: 15px 10px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; }
    .item-title { font-size: 1.1em; font-weight: 500; }
    .main .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def get_dummy_content(filename):
    return f"This is a placeholder file for {filename}."

# --- Data Source (Formula Sheet Removed) ---
units = [
    {"num": 1, "title": "Atomic Structure and Periodic Table", "desc": "Subatomic Particles, Electron Configuration, Periodic Trends", "files": {"Lecture Notes": "Unit 1.pdf", "Exercises": "Unit 1 - Exercises.pdf", "Answer Key": "Unit 1 - Key.pdf"}},
    {"num": 2, "title": "Chemical Bonding and Molecular Structure", "desc": "Ionic & Covalent Bonding, VSEPR, Intermolecular Forces", "files": {"Lecture Notes": "Unit 2.pdf", "Exercises": "Unit 2 - Exercises.pdf", "Answer Key": "Unit 2 - Key.pdf"}},
    {"num": 3, "title": "Stoichiometry and Chemical Calculations", "desc": "Mole Concept, Empirical Formulas, Limiting Reactants", "files": {"Lecture Notes": "Unit 3.pdf", "Exercises": "Unit 3 - Exercises.pdf", "Answer Key": "Unit 3 - Key.pdf"}},
    {"num": 4, "title": "States of Matter and Solutions", "desc": "Gas Laws, Solubility, Colligative Properties", "files": {"Lecture Notes": "Unit 4.pdf", "Exercises": "Unit 4 - Exercises.pdf", "Answer Key": "Unit 4 - Key.pdf"}},
    {"num": 5, "title": "Thermodynamics", "desc": "Enthalpy, Entropy, Gibbs Free Energy", "files": {"Lecture Notes": "Unit 5.pdf", "Exercises": "Unit 5 - Exercises.pdf", "Answer Key": "Unit 5 - Key.pdf"}},
    {"num": 6, "title": "Chemical Kinetics", "desc": "Rate Laws, Activation Energy, Reaction Mechanisms", "files": {"Lecture Notes": "Unit 6.pdf", "Exercises": "Unit 6 - Exercises.pdf", "Answer Key": "Unit 6 - Key.pdf"}},
    {"num": 7, "title": "Chemical Equilibrium", "desc": "Equilibrium Constant, Le Chatelier's Principle, Solubility Product", "files": {"Lecture Notes": "Unit 7.pdf", "Exercises": "Unit 7 - Exercises.pdf", "Answer Key": "Unit 7 - Key.pdf"}},
    {"num": 8, "title": "Acids and Bases", "desc": "pH Calculations, Titrations, Buffer Solutions, Salt Hydrolysis", "files": {"Lecture Notes": "Unit 8.pdf", "Exercises": "Unit 8 - Exercises.pdf", "Answer Key": "Unit 8 - Key.pdf"}},
    {"num": 9, "title": "Inorganic Chemistry", "desc": "Main Group Elements, Coordination Compounds, Crystal Field Theory", "files": {"Lecture Notes": "Unit 9.pdf", "Exercises": "Unit 9 - Exercises.pdf", "Answer Key": "Unit 9 - Key.pdf"}},
    {"num": 10, "title": "Introductory Organic Chemistry", "desc": "Functional Groups, Isomerism, Reaction Mechanisms", "files": {"Lecture Notes": "Unit 10.pdf", "Exercises": "Unit 10 - Exercises.pdf", "Answer Key": "Unit 10 - Key.pdf"}}
]

# --- MAIN PAGE LOGIC ---
st.title("👨‍🏫 Chemistry Lecture")
st.markdown("### Course Units")

for unit in units:
    with st.container():
        col_title, col_controls = st.columns([6, 4])
        
        with col_title:
            st.markdown(f"<div class='item-title'>Unit {unit['num']}: {unit['title']}</div>", unsafe_allow_html=True)
            st.caption(unit['desc'])
        
        with col_controls:
            c_select, c_btn = st.columns([2, 1])
            
            with c_select:
                file_options = list(unit['files'].keys())
                selection = st.selectbox("File", file_options, key=f"select_{unit['num']}", label_visibility="collapsed")
            
            with c_btn:
                if selection:
                    filename = unit['files'][selection]
                    st.download_button("Download", data=get_dummy_content(filename), file_name=filename, key=f"dl_{unit['num']}")
        
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)