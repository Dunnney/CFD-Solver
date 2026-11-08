from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from cfdkit.case import load_case

CASE_FILE = Path(__file__).parent.parent / "cases" / "sod_tube.yaml"

def _load_raw():
    with open(CASE_FILE) as f:
        return yaml.safe_load(f)
    
def _write(tmp_path, data):
    p = tmp_path / "case.yaml"
    p.write_text(yaml.safe_dump(data))
    return p

def test_sod_tube_loads():
    case = load_case(CASE_FILE)
    assert case.name == "sod_tube"
    assert case.physics.gas.gamma == 1.4
    assert case.numerics.cfl == 0.5

def test_typo_in_scheme_is_rejected(tmp_path):
    data = _load_raw()
    data["numerics"]["flux_scheme"] = "hlcc" 
    with pytest.raises(ValidationError):
        load_case(_write(tmp_path, data))

def test_negative_cfl_is_rejected(tmp_path):
    data = _load_raw()
    data["numerics"]["cfl"] = -3
    with pytest.raises(ValidationError):
        load_case(_write(tmp_path, data))


def test_unknown_key_is_rejected(tmp_path):
    data = _load_raw()
    data["numerics"]["flux_sheme"] = "roe"
    with pytest.raises(ValidationError):
        load_case(_write(tmp_path, data))


def test_bad_mesh_bounds_are_rejected(tmp_path):
    data = _load_raw()
    data["mesh"]["x_min"], data["mesh"]["x_max"] = 1.0, 0.0
    with pytest.raises(ValidationError):
        load_case(_write(tmp_path, data))