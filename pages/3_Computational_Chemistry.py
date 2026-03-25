import streamlit as st
import streamlit.components.v1 as components

# --- Imports ---
try:
    from pyscf import gto, scf
    from pyscf.geomopt.geometric_solver import optimize as geom_optimize
    from rdkit import Chem
    from rdkit.Chem import AllChem
    import py3Dmol
    import numpy as np
    PYSCF_READY = True
except ImportError:
    PYSCF_READY = False

# --- Page Configuration ---
st.set_page_config(page_title="Computational Chemistry - ChemieLearn", layout="wide")

st.title("💻 Computational Chemistry")
st.markdown("### Quantum Chemistry with PySCF")

if not PYSCF_READY:
    st.error("⚠️ **Libraries missing.** Please install `pyscf`, `geometric`, `rdkit`, and `py3Dmol`.")
    st.code("pip install pyscf geometric rdkit py3Dmol", language='bash')
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
            # Fallback to UFF if MMFF fails
            try:
                AllChem.UFFOptimizeMolecule(mol)
            except:
                pass

        # Convert to XYZ string
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

def run_pyscf_optimization(xyz_string, method, basis):
    """
    Runs PySCF geometry optimization.
    Returns: Final Energy, Optimized XYZ string.
    """
    try:
        # 1. Build PySCF Molecule
        # PySCF requires geometry in a specific format (units Angstrom)
        mol = gto.M(atom=xyz_string, basis=basis, unit='Angstrom', charge=0, spin=0)
        
        # 2. Define Method
        if method == "HF":
            mf = scf.RHF(mol)
        elif method == "B3LYP":
            # DFT requires defining the functional
            mf = scf.RKS(mol)
            mf.xc = 'b3lyp'
        else:
            return None, None, "Method not supported."

        # 3. Run Optimization
        # 'geometric' library handles the optimization loop
        # We set max steps to keep it fast for web demo
        opt_config = {'convergence_set': 'GAU'} 
        
        # Run optimization
        # Note: PySCF geomopt returns the new molecule object
        mol_eq = geom_optimize(mf, **opt_config)
        
        # 4. Get Final Energy
        final_energy = mf.e_tot

        # 5. Extract Optimized Geometry
        # PySCF stores geometry in mol_eq.atom_coords() (Bohr usually)
        coords = mol_eq.atom_coords(unit='Angstrom')
        symbols = [mol_eq.atom_symbol(i) for i in range(mol_eq.natm)]
        
        opt_xyz_lines = []
        for i in range(mol_eq.natm):
            opt_xyz_lines.append(f"{symbols[i]} {coords[i][0]:.6f} {coords[i][1]:.6f} {coords[i][2]:.6f}")
        
        opt_xyz = "\n".join(opt_xyz_lines)
        
        return final_energy, opt_xyz, "Calculation Successful."
        
    except Exception as e:
        return None, None, f"PySCF Error: {str(e)}"

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
            st.error(xyz_data) 
        else:
            with st.expander("👁️ View Pre-optimized Input Structure"):
                view = draw_3d(xyz_data)
                components.html(view._make_html(), width=400, height=300, scrolling=False)

            # Step 2: PySCF Optimization
            progress_bar = st.progress(0)
            progress_bar.progress(50)
            
            with st.spinner(f"2. Running PySCF Optimization ({method}/{basis})..."):
                energy, opt_xyz, log_msg = run_pyscf_optimization(xyz_data, method, basis)
            
            progress_bar.progress(100)

            if energy:
                st.success("✅ Calculation Complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Results")
                    st.metric("Final Energy", f"{energy:.6f} Hartree")
                    st.info(f"Method: {method}/{basis}")
                    
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