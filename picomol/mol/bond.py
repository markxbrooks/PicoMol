from dataclasses import dataclass


@dataclass
class Bond:
    """Represents a bond between two atoms"""
    atom1_idx: int
    atom2_idx: int
    bond_type: str = "single"  # single, double, triple, aromatic