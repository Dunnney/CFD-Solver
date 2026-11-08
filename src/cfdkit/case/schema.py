from pathlib import Path
from typing import Dict, List, Literal, Optional, Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    """Base class that rejects unknown keys."""
    model_config = ConfigDict(extra="forbid")

class Gas(StrictModel):
    gamma: float = Field(gt=1.0)
    gas_constant: float = Field(gt=0.0)

class Physics(StrictModel):
    model: Literal["euler"]
    dimension: Literal[1]
    gas: Gas

class Mesh(StrictModel):
    type: Literal["structured_1d"]
    n_cells: int = Field(gt=1)
    x_min: float
    x_max: float

    @model_validator(mode="after")
    def check_bounds(self):
        if self.x_max <= self.x_min:
            raise ValueError("mesh x_max must be greater than x_min")
        return self
    
class Region(StrictModel):
    x_min: Optional[float] = None
    x_max: Optional[float] = None

class InitialCondition(StrictModel):
    region: Region
    density: float = Field(gt=0.0)
    velocity: float
    pressure: float = Field(gt=0.0)

class BoundaryCondition(StrictModel):
    type: Literal["outflow", "wall", "inflow"]

class BoundaryConditions(StrictModel):
    left: BoundaryCondition
    right: BoundaryCondition

class Numerics(StrictModel):
    flux_scheme: Literal["roe", "hllc"]
    reconstruction: Literal["constant", "muscl"]
    limiter: Literal["minmod", "vanleer"]
    time_integrator: Literal["euler", "rk2", "rk3"]
    cfl: float = Field(gt=0.0, le=1.0)
    end_time: float = Field(gt=0.0)

class Case(StrictModel):
    name: str
    physics: Physics
    mesh: Mesh
    initial_conditions: List[InitialCondition] = Field(min_length=1)
    boundary_conditions: BoundaryConditions
    numerics: Numerics
    passthrough: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

def load_case(path) -> Case:
    """Read a YAML file and return a validated Case."""
    with open(Path(path)) as f:
        data = yaml.safe_load(f)
    return Case(**data)
