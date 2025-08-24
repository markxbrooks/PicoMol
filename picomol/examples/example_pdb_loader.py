"""
PDB File Loader for MolViewSpec Integration

This module provides functionality to:
1. Load and parse PDB files
2. Convert PDB data to MolViewSpec format
3. Integrate with PicoGL's molecular visualization system
"""

from picomol.loader.pdb import PDBLoader
from picomol.molviewspec.save import save_molviewspec
from picomol.logger import setup_logging, Logger as log

if __name__ == "__main__":
    # Example usage
    try:
        # Load a PDB file
        setup_logging()
        loader = PDBLoader("examples/data/2VUG.pdb")
        
        log.message(f"Loaded structure: {loader.structure.title}")
        log.message(f"Atoms: {len(loader.structure.atoms)}")
        log.message(f"Bonds: {len(loader.structure.bonds)}")
        log.message(f"Residues: {len(loader.structure.residues)}")
        log.message(f"Chains: {loader.structure.chains}")
        
        # Convert to MolViewSpec
        molviewspec = loader.to_molviewspec()
        save_molviewspec(molviewspec, "../loader/output.molviewspec")
        log.message("Saved MolViewSpec file: output.molviewspec")
        
        # Convert to PicoGL data
        picogl_data = loader.to_picogl_data()
        log.message(f"PicoGL data: {picogl_data['atoms']['count']} atoms, {picogl_data['bonds']['count']} bonds")
        
    except FileNotFoundError as e:
        log.message(f"Error: {e}")
        log.message("Make sure you have a PDB file in the data/ directory")
    except Exception as e:
        log.message(f"Error: {e}")
