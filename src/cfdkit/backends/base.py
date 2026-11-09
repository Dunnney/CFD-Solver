from abc import ABC, abstractmethod
from pathlib import Path

from cfdkit.case import Case
from cfdkit.results import Results


class Backend(ABC):
    """Every solver adapter implements these three steps."""

    name: str = "unnamed"

    @abstractmethod
    def write_case(self, case: Case, workdir: Path) -> None:
        """Translate the validated Case into this solver's input files."""

    @abstractmethod
    def run(self, workdir: Path) -> None:
        """Run the solver inside workdir."""

    @abstractmethod
    def read_results(self, workdir: Path) -> Results:
        """Read the solver's output into the common Results container."""

    def execute(self, case: Case, workdir) -> Results:
        """Full pipeline: write, run, read."""
        workdir = Path(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        self.write_case(case, workdir)
        self.run(workdir)
        return self.read_results(workdir)