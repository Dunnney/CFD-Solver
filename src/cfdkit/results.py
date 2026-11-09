from dataclasses import dataclass, field
from typing import Dict

import numpy as np


@dataclass
class Results:
    """Solver-independent description of a finished run."""
    x: np.ndarray                      # cell-centre coordinates
    time: float                        # simulation time of the snapshot
    fields: Dict[str, np.ndarray] = field(default_factory=dict)
    # e.g. {"density": ..., "velocity": ..., "pressure": ...}