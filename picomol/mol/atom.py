from dataclasses import dataclass


@dataclass
class Atom:
    """Represents a single atom from a PDB file"""
    serial: int
    name: str
    res_name: str
    chain_id: str
    res_seq: int
    x: float
    y: float
    z: float
    element: str
    charge: str = ""
    occupancy: float = 1.0
    b_factor: float = 0.0