from dataclasses import dataclass
from typing import List

import numpy as np

from picomol.mol.atom import Atom
from picomol.mol.bond import Bond
from picomol.mol.residue import Residue


@dataclass
class PDBStructure:
    """Complete PDB structure data"""
    title: str
    atoms: List[Atom]
    bonds: List[Bond]
    residues: List[Residue]
    chains: List[str]

    def get_atom_positions(self) -> np.ndarray:
        """Get all atom positions as a numpy array"""
        return np.array([[atom.x, atom.y, atom.z] for atom in self.atoms], dtype=np.float32)

    def get_atom_elements(self) -> List[str]:
        """Get all atom element symbols"""
        return [atom.element for atom in self.atoms]

    def get_residue_atoms(self, residue_idx: int) -> List[Atom]:
        """Get atoms for a specific residue"""
        if 0 <= residue_idx < len(self.residues):
            return self.residues[residue_idx].atoms
        return []