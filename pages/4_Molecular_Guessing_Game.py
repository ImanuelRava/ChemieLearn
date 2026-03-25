import streamlit as st
import streamlit.components.v1 as components
import random

# --- Imports ---
try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    import py3Dmol
    GAME_READY = True
except ImportError:
    GAME_READY = False

# --- Page Configuration ---
st.set_page_config(page_title="Molecular Guessing Game - ChemieLearn", layout="wide", page_icon="favicon.ico")

st.title("🎮 Molecular Guessing Game")
st.markdown("Can you identify the molecule from its 3D structure?")

if not GAME_READY:
    st.error("Libraries missing. Please install `rdkit` and `py3Dmol`.")
    st.stop()

# --- Game Data ---
# A comprehensive list of molecules with their SMILES and common names
MOLECULES = [
    # Basics
    {"name": "Water", "smiles": "O", "hint": "Essential for life (H2O)."},
    {"name": "Carbon Dioxide", "smiles": "O=C=O", "hint": "We breathe this out."},
    {"name": "Ammonia", "smiles": "N", "hint": "Common cleaning agent (NH3)."},
    {"name": "Methane", "smiles": "C", "hint": "Main component of natural gas."},
    
    # Simple Organics
    {"name": "Ethanol", "smiles": "CCO", "hint": "Found in alcoholic beverages."},
    {"name": "Acetone", "smiles": "CC(=O)C", "hint": "Nail polish remover."},
    {"name": "Acetic Acid", "smiles": "CC(=O)O", "hint": "Found in vinegar."},
    {"name": "Formaldehyde", "smiles": "C=O", "hint": "Used for preserving specimens."},
    {"name": "Formic Acid", "smiles": "O=CO", "hint": "Found in ant stings."},
    
    # Hydrocarbons
    {"name": "Propane", "smiles": "CCC", "hint": "Used in gas grills."},
    {"name": "Butane", "smiles": "CCCC", "hint": "Found in cigarette lighters."},
    {"name": "Ethylene", "smiles": "C=C", "hint": "Ripens fruit."},
    {"name": "Acetylene", "smiles": "C#C", "hint": "Used in welding torches."},
    
    # Aromatics
    {"name": "Benzene", "smiles": "c1ccccc1", "hint": "The simplest aromatic ring."},
    {"name": "Toluene", "smiles": "Cc1ccccc1", "hint": "Paint thinner smell."},
    {"name": "Phenol", "smiles": "Oc1ccccc1", "hint": "Antiseptic in hospitals."},
    {"name": "Naphthalene", "smiles": "c1ccc2ccccc2c1", "hint": "Old-fashioned mothballs."},
    
    # Biomolecules & Famous Molecules
    {"name": "Caffeine", "smiles": "Cn1cnc2c1c(=O)n(c(=O)n2C)C", "hint": "Keeps you awake."},
    {"name": "Aspirin", "smiles": "CC(=O)Oc1ccccc1C(=O)O", "hint": "Common pain reliever."},
    {"name": "Paracetamol", "smiles": "CC(=O)Nc1ccc(O)cc1", "hint": "Tylenol or Panadol."},
    {"name": "Nicotine", "smiles": "CN1CCCC1c2cccnc2", "hint": "Addictive component in tobacco."},
    {"name": "Vitamin C", "smiles": "OC[C@H]1O[C@@H](C(=O)O)C(O)=C1O", "hint": "Found in oranges."},
    {"name": "Citric Acid", "smiles": "OC(=O)CC(O)(CC(=O)O)C(=O)O", "hint": "Gives lemons their sour taste."},
    {"name": "Glucose", "smiles": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O", "hint": "Simple blood sugar."},
    {"name": "Urea", "smiles": "NC(=O)N", "hint": "First organic synthesis."},
    
    # Drugs & Interesting Structures
    {"name": "Ibuprofen", "smiles": "CC(C)Cc1ccc(cc1)C(C)C(=O)O", "hint": "Anti-inflammatory (Advil)."},
    {"name": "Dopamine", "smiles": "NCCc1ccc(O)c(O)c1", "hint": "The 'feel-good' neurotransmitter."},
    {"name": "Adrenaline", "smiles": "CNC[C@H](O)c1ccc(O)c(O)c1", "hint": "Fight or flight hormone."},
    {"name": "Morphine", "smiles": "CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O", "hint": "Powerful painkiller."},
    
    # Others
    {"name": "Chloroform", "smiles": "ClC(Cl)Cl", "hint": "Used in movies to knock people out."},
    {"name": "Trinitrotoluene", "smiles": "Cc1c(cc(cc1[N+](=O)[O-])[N+](=O)[O-])[N+](=O)[O-]", "hint": "Also known as TNT."}
]

# --- Helper Functions ---

def generate_3d_view(smiles, width=500, height=400):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol: return None
        mol = Chem.AddHs(mol)
        res = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
        if res == -1: return None
        AllChem.UFFOptimizeMolecule(mol)
        
        mol_block = Chem.MolToMolBlock(mol)
        view = py3Dmol.view(width=width, height=height)
        view.addModel(mol_block, "mol")
        view.setStyle({'stick': {}})
        view.zoomTo()
        view.spin(True) # Enable continuous spinning
        return view
    except:
        return None

def new_game():
    st.session_state.score = 0
    st.session_state.round = 1
    st.session_state.history = []
    next_molecule()

def next_molecule():
    # Select a random molecule not recently used
    available = [m for m in MOLECULES if m['name'] not in st.session_state.history]
    if not available:
        st.session_state.history = [] # Reset history if all used
        available = MOLECULES
        
    current = random.choice(available)
    st.session_state.current_mol = current
    st.session_state.history.append(current['name'])
    st.session_state.guessed = False
    st.session_state.attempts = 0

# --- Session State Initialization ---
if 'current_mol' not in st.session_state:
    new_game()

# --- Sidebar ---
st.sidebar.metric("Score", st.session_state.score)
st.sidebar.metric("Round", st.session_state.round)
if st.sidebar.button("🔄 Restart Game"):
    new_game()

# --- Main Game Area ---

# 1. Display 3D Structure
current = st.session_state.current_mol
view = generate_3d_view(current['smiles'])

if view:
    components.html(view._make_html(), width=500, height=400, scrolling=False)
else:
    st.error("Could not generate 3D structure.")

# 2. Game Logic
if not st.session_state.guessed:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_guess = st.text_input("Your Guess:", placeholder="Type the molecule name...", key="guess_input")
        
        if st.button("Submit Guess"):
            # Normalize strings for comparison
            guess_clean = user_guess.strip().lower()
            answer_clean = current['name'].strip().lower()
            
            if guess_clean == answer_clean:
                st.session_state.score += 1
                st.session_state.guessed = True
                st.balloons()
            else:
                st.session_state.attempts += 1
                st.warning("Incorrect! Try again.")
    
    with col2:
        st.info(f"💡 **Hint:** {current['hint']}")
        if st.session_state.attempts >= 2:
            st.error(f"😫 Tough one? The answer starts with **{current['name'][0]}**")

else:
    # Correct Answer State
    st.success(f"🎉 Correct! It was **{current['name']}**.")
    if st.button("Next Molecule ➡️"):
        st.session_state.round += 1
        next_molecule()