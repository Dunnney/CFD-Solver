from pathlib import Path

import numpy as np
import pytest

from cfdkit.backends.base import Backend
from cfdkit.case import load_case
from cfdkit.results import Results

CASE_FILE = Path(__file__).parent.parent / "cases" / "sod_tube.yaml"


class DummyBackend(Backend):
    name = "dummy"

    def write_case(self, case, workdir):
        (workdir / "input.txt").write_text(case.name)

    def run(self, workdir):
        (workdir / "output.txt").write_text("done")

    def read_results(self, workdir):
        x = np.linspace(0, 1, 5)
        return Results(x=x, time=0.0, fields={"density": np.ones(5)})


def test_execute_runs_full_pipeline(tmp_path):
    case = load_case(CASE_FILE)
    results = DummyBackend().execute(case, tmp_path / "run1")
    assert (tmp_path / "run1" / "input.txt").read_text() == "sod_tube"
    assert (tmp_path / "run1" / "output.txt").exists()
    assert results.fields["density"].shape == (5,)


def test_incomplete_backend_cannot_be_created():
    class Broken(Backend):
        def write_case(self, case, workdir):
            pass

    with pytest.raises(TypeError):
        Broken()