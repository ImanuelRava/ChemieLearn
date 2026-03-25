import streamlit as st
import streamlit.components.v1 as components

# --- Imports ---
try:
    import psi4
    from rdkit import Chem
    from rdkit.Chem import AllChem
    import py3Dmol
    PSI4_READY = True
except ImportError:
    PSI4_READY = False

# --- Page Configuration ---
st.set_page_config(page_title="Computational Chemistry - ChemieLearn", layout="wide")

st.title("💻 Computational Chemistry")
st.markdown("### Quantum Chemistry with Psi4")

if not PSI4_READY:
    st.error("⚠️ **Libraries missing.** Please install `psi4`, `rdkit`, and `py3Dmol`.")
    st.code("pip install psi4 rdkit py3Dmol", language='bash')
    st.stop()

# --- Helper Functions ---

def rdkit_pre_optimization(smiles):
    """
    1. Generates 3D coordinates from SMILES.
    2. Pre-optimizes using MMFF94s.
    Returns: RDKit Mol object and XYZ string.
    """
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return None, "Invalid SMILES string."
        
        mol = Chem.AddHs(mol)
        
        # Check Atom Count Limit
        num_atoms = mol.GetNumAtoms()
        if num_atoms > 20:
            return None, f"**Atom limit exceeded:** {num_atoms} atoms found. Maximum allowed is 20."
        
        # Generate 3D Coordinates
        res = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
        if res == -1:
            return None, "Could not generate 3D coordinates."
            
        # Pre-optimization with MMFF94s
        try:
            AllChem.MMFFOptimizeMolecule(mol)
        except:
            # Fallback to UFF if MMFF fails (e.g., for some metal complexes)
            try:
                AllChem.UFFOptimizeMolecule(mol)
            except:
                pass # Proceed with unoptimized if force fields fail

        # Convert to XYZ string for Psi4
        xyz_lines = []
        conf = mol.GetConformer()
        for i in range(num_atoms):
            atom = mol.GetAtomWithIdx(i)
            symbol = atom.GetSymbol()
            pos = conf.GetAtomPosition(i)
            xyz_lines.append(f"{symbol} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}")
            
        return mol, "\n".join(xyz_lines)
        
    except Exception as e:
        return None, f"RDKit Error: {str(e)}"

def run_psi4_optimization(xyz_string, method, basis):
    """
    Runs Psi4 geometry optimization.
    Returns: Final Energy, Log, and Optimized XYZ coordinates.
    """
    try:
        # Clean previous runs
        psi4.core.clean()
        psi4.set_memory('500 MB')
        psi4.set_num_threads(2)
        
        # Define Molecule (assuming charge 0, multiplicity 1 for simplicity)
        mol = psi4.geometry(f"""
        {xyz_string}
        symmetry c1
        """)
        
        # Set options
        psi4.set_options({
            'basis': basis,
            'scf_type': 'df',
            'e_convergence': 1e-5,
            'g_convergence': 'gau_loose'
        })
        
        # Run Optimization
        energy = psi4.optimize(f'{method}/{basis}', molecule=mol)
        
        # Get optimized geometry
        optimized_xyz = mol.save_string_xyz()
        
        return energy, optimized_xyz, "Calculation Successful."
        
    except Exception as e:
        return None, None, f"Psi4 Error: {str(e)}"

def draw_3d(xyz_string, width=500, height=400):
    view = py3Dmol.view(width=width, height=height)
    view.addModel(xyz_string, "xyz")
    view.setStyle({'stick': {}})
    view.zoomTo()
    return view

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Settings")
method = st.sidebar.selectbox("Method", ["HF", "B3LYP"], index=0)
basis = st.sidebar.selectbox("Basis Set", ["sto-3g", "6-31g"], index=0)

# --- Main Input ---
st.markdown("Enter a **SMILES** string to calculate geometry and energy.")
st.warning("⚠️ **Limit:** Maximum 20 atoms (including Hydrogens).")

examples = {"Water (3 atoms)": "O", "Methane (5 atoms)": "C", "Ethanol (9 atoms)": "CCO"}
selected = st.selectbox("Quick Examples:", [""] + list(examples.keys()))
default_smiles = examples.get(selected, "")

smiles_input = st.text_input("SMILES Input:", value=default_smiles, placeholder="e.g., O for water")

# --- Process ---
if st.button("🚀 Run Calculation"):
    if not smiles_input:
        st.warning("Please enter a SMILES string.")
    else:
        # Step 1: RDKit Pre-optimization
        with st.spinner("1. Generating 3D geometry & Pre-optimizing (MMFF94s)..."):
            rdkit_mol, xyz_data = rdkit_pre_optimization(smiles_input)
        
        if not rdkit_mol:
            st.error(xyz_data) # Error message is returned in xyz_data variable
        else:
            # Display Initial Structure
            with st.expander("👁️ View Pre-optimized Input Structure"):
                # Convert rdkit mol to xyz for viewing
                init_xyz = xyz_data
                view = draw_3d(init_xyz)
                components.html(view._make_html(), width=400, height=300, scrolling=False)

            # Step 2: Psi4 Optimization
            progress_bar = st.progress(0)
            progress_bar.progress(50)
            
            with st.spinner(f"2. Running Psi4 Optimization ({method}/{basis})..."):
                energy, opt_xyz, log_msg = run_psi4_optimization(xyz_data, method, basis)
            
            progress_bar.progress(100)

            if energy:
                st.success("✅ Calculation Complete!")
                
                # Display Results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Results")
                    st.metric("Final Energy", f"{energy:.6f} Hartree")
                    st.info(f"Method: {method}/{basis}")
                    
                    # Download button for XYZ
                    st.download_button(
                        label="📥 Download Optimized Coordinates (.xyz)",
                        data=opt_xyz,
                        file_name=f"optimized_{smiles_input}.xyz",
                        mime="text/plain"
                    )
                
                with col2:
                    st.subheader("🔬 Optimized Structure")
                    view = draw_3d(opt_xyz)
                    components.html(view._make_html(), width=400, height=400, scrolling=False)
            
            else:
                st.error(log_msg)

else:
    st.info("Adjust settings in the sidebar and click 'Run Calculation'.")