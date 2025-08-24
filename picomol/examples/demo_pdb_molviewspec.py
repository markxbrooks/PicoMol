#!/usr/bin/env python3
"""
PDB to MolViewSpec Conversion Demo

This script demonstrates how to:
1. Load PDB files
2. Convert them to MolViewSpec format
3. Save the results for portable viewing
"""

import os
import sys
import json
from pathlib import Path

from picomol.loader.pdb import PDBLoader
from picomol.logger import setup_logging, Logger as log
from picomol.molviewspec.save import save_molviewspec

# Add the utils directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))


def download_sample_pdb():
    """Download a sample PDB file for demonstration"""
    import urllib.request
    
    # Download a small protein structure (Crambin - 46 residues)
    pdb_id = "1CRN"
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    output_file = f"data/{pdb_id}.pdb"
    
    log.message(f"Downloading {pdb_id} from RCSB PDB...")
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs("../../examples/data", exist_ok=True)
        
        # Download the file
        urllib.request.urlretrieve(url, output_file)
        log.message(f"✓ Downloaded {pdb_id}.pdb successfully")
        return output_file
        
    except Exception as e:
        log.message(f"✗ Failed to download {pdb_id}.pdb: {e}")
        return None


def analyze_structure(loader):
    """Analyze the loaded structure and print statistics"""
    structure = loader.structure
    
    log.message(f"\n📊 Structure Analysis:")
    log.message(f"  Title: {structure.title}")
    log.message(f"  Total Atoms: {len(structure.atoms)}")
    log.message(f"  Total Bonds: {len(structure.bonds)}")
    log.message(f"  Total Residues: {len(structure.residues)}")
    log.message(f"  Chains: {', '.join(structure.chains) if structure.chains else 'None'}")
    
    # Analyze atom types
    elements = {}
    for atom in structure.atoms:
        elements[atom.element] = elements.get(atom.element, 0) + 1
    
    log.message(f"  Element Composition:")
    for element, count in sorted(elements.items()):
        log.message(f"    {element}: {count}")
    
    # Analyze residue types
    residues = {}
    for residue in structure.residues:
        residues[residue.name] = residues.get(residue.name, 0) + 1
    
    log.message(f"  Residue Types:")
    for residue, count in sorted(residues.items()):
        log.message(f"    {residue}: {count}")


def export_formats(loader, base_name):
    """Export the structure in multiple formats"""
    log.message(f"\n💾 Exporting Structure...")
    
    # Export to MolViewSpec
    molviewspec_file = f"{base_name}.molviewspec"
    molviewspec = loader.to_molviewspec()
    save_molviewspec(molviewspec, molviewspec_file)
    log.message(f"  ✓ MolViewSpec: {molviewspec_file}")
    
    # Export to PicoGL data
    picogl_data = loader.to_picogl_data()
    picogl_file = f"{base_name}_picogl.json"
    with open(picogl_file, 'w') as f:
        json.dump(picogl_data, f, indent=2)
    log.message(f"  ✓ PicoGL Data: {picogl_file}")
    
    # Export summary
    summary_file = f"{base_name}_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(f"Structure Summary: {loader.structure.title}\n")
        f.write(f"Atoms: {len(loader.structure.atoms)}\n")
        f.write(f"Bonds: {len(loader.structure.bonds)}\n")
        f.write(f"Residues: {len(loader.structure.residues)}\n")
        f.write(f"Chains: {', '.join(loader.structure.chains)}\n")
    log.message(f"  ✓ Summary: {summary_file}")


def show_molviewspec_info(molviewspec):
    """Display information about the generated MolViewSpec"""
    log.message(f"\n🔍 MolViewSpec Information:")
    log.message(f"  Version: {molviewspec.get('version', 'Unknown')}")
    log.message(f"  Name: {molviewspec.get('name', 'Unknown')}")
    log.message(f"  Description: {molviewspec.get('description', 'None')}")
    log.message(f"  Components: {len(molviewspec.get('components', []))}")
    
    for i, component in enumerate(molviewspec.get('components', [])):
        comp_type = component.get('type', 'Unknown')
        comp_kind = component.get('kind', 'Unknown')
        log.message(f"    Component {i+1}: {comp_type} - {comp_kind}")


def main():
    """Main demonstration function"""
    setup_logging()
    log.message("🧬 PDB to MolViewSpec Conversion Demo")
    log.message("=" * 50)
    
    # Check if we have a PDB file
    pdb_files = []
    
    # Look for PDB files in the data directory
    data_dir = Path("../../examples/data")
    if data_dir.exists():
        pdb_files = list(data_dir.glob("*.pdb"))
    
    if not pdb_files:
        log.message("No PDB files found in data/ directory.")
        log.message("Downloading a sample PDB file...")
        
        sample_file = download_sample_pdb()
        if sample_file:
            pdb_files = [Path(sample_file)]
        else:
            log.message("Could not download sample PDB file.")
            log.message("Please place a PDB file in the data/ directory and run again.")
            return
    
    # Process each PDB file
    for pdb_file in pdb_files:
        log.message(f"\n📁 Processing: {pdb_file.name}")
        log.message("-" * 30)
        
        try:
            # Load the PDB file
            loader = PDBLoader(str(pdb_file))
            
            # Analyze the structure
            analyze_structure(loader)
            
            # Export in various formats
            base_name = pdb_file.stem
            export_formats(loader, base_name)
            
            # Show MolViewSpec information
            molviewspec = loader.to_molviewspec()
            show_molviewspec_info(molviewspec)
            
            log.message(f"\n✅ Successfully processed {pdb_file.name}")
            
        except Exception as e:
            log.message(f"❌ Error processing {pdb_file.name}: {e}")
            import traceback
            traceback.print_exc()
    
    log.message(f"\n🎉 Demo completed!")
    log.message(f"\nNext steps:")
    log.message(f"1. Open the .molviewspec files in Mol* Viewer (https://molstar.org/)")
    log.message(f"2. Use the PicoGL data for custom visualization")
    log.message(f"3. Share the MolViewSpec files with colleagues")


if __name__ == "__main__":
    main()
