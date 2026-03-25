import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
import py3Dmol
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(page_title="Chemical Structure Visualizer - ChemieLearn", layout="wide")

st.title("🔬 Chemical Structure Visualizer")
st.markdown("Use this tool to visualize structures in **2D** and interactive **3D** from SMILES strings.")

# --- Helper Functions ---

def smiles_to_2d_img(smiles_string, size=(400, 400)):
    """Generates a 2D image using RDKit."""
    try:
        mol = Chem.MolFromSmiles(smiles_string)
        if mol:
            AllChem.Compute2DCoords(mol)
            img = Draw.MolToImage(mol, size=size)
            return img
    except:
        pass
    return None

def generate_3d_view(smiles_string, width=500, height=500):
    """
    Generates an interactive 3D view using py3Dmol.
    Returns HTML component.
    """
    try:
        # 1. Parse SMILES
        mol = Chem.MolFromSmiles(smiles_string)
        if not mol:
            return None

        # 2. Add Hydrogens (Crucial for correct 3D geometry)
        mol = Chem.AddHs(mol)

        # 3. Generate 3D Coordinates
        res = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
        
        if res == -1:
            return None

        # 4. Optimize Geometry
        AllChem.UFFOptimizeMolecule(mol)

        # 5. Convert to MolBlock format
        mol_block = Chem.MolToMolBlock(mol)

        # 6. Create py3Dmol view
        view = py3Dmol.view(width=width, height=height)
        view.addModel(mol_block, "mol")
        
        # Style the molecule
        view.setStyle({'stick': {}})
        view.zoomTo()
        
        return view
    except Exception as e:
        st.error(f"3D Generation Error: {e}")
        return None

# --- Main Input ---
# Fixed size for the viewer (removed slider)
VIEWER_WIDTH = 500
VIEWER_HEIGHT = 500

smiles_input = st.text_input("Enter SMILES String:", placeholder="e.g., CCO for Ethanol")

# --- Processing ---
if smiles_input:
    st.info(f"SMILES: `{smiles_input}`")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # --- Column 1: 2D Image ---
    with col1:
        st.subheader("2D Structure")
        img_2d = smiles_to_2d_img(smiles_input, size=(VIEWER_WIDTH, VIEWER_HEIGHT))
        if img_2d:
            st.image(img_2d)
            
            # Download Button for 2D
            buf = BytesIO()
            img_2d.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="📥 Download 2D (PNG)",
                data=byte_im,
                file_name=f"2d_{smiles_input}.png",
                mime="image/png",
                key="dl_2d"
            )
        else:
            st.error("Could not generate 2D image.")

    # --- Column 2: 3D Interactive Viewer ---
    with col2:
        st.subheader("3D Interactive Model")
        view = generate_3d_view(smiles_input, width=VIEWER_WIDTH, height=VIEWER_HEIGHT)
        
        if view:
            # Render py3Dmol viewer
            components.html(view._make_html(), width=VIEWER_WIDTH, height=VIEWER_HEIGHT, scrolling=False)
            st.caption("🖱️ **Interact:** Drag to rotate, scroll to zoom.")
        else:
            st.warning("Could not generate 3D coordinates.")

else:
    st.warning("Please enter a SMILES string to visualize the structure.")

# --- Footer Info ---
st.markdown("---")
st.markdown("""
**How it works:**
1. **2D Structure:** Calculated using RDKit standard coordinates.
2. **3D Model:** Hydrogens are added automatically. RDKit generates an initial 3D conformation and optimizes the geometry.
""")