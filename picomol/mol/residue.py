from dataclasses import dataclass
from typing import List

from picomol.mol.atom import Atom


@dataclass
class Residue:
    """Represents a residue/amino acid"""
    name: str
    chain_id: str
    seq_num: int
    atoms: List[Atom]
    start_idx: int  # Index in the main atom list