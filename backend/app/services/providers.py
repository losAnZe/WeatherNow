from abc import ABC, abstractmethod
from typing import Any

class DataProvider(ABC):
    name: str
    @abstractmethod
    def status(self) -> dict[str, str]: ...

class DemoProvider(DataProvider):
    def __init__(self, name: str): self.name = name
    def status(self) -> dict[str, str]: return {"provider": self.name, "mode": "DEMO", "status": "READY"}

class FutureRealProvider(DataProvider):
    """Implement authenticated ingestion, provenance, QC and freshness checks for a real provider."""
    def __init__(self, name: str): self.name = name
    def status(self) -> dict[str, str]: return {"provider": self.name, "mode": "NOT_CONFIGURED", "status": "OFFLINE"}

PROVIDERS = [DemoProvider(name) for name in ("INSAT", "IMDAA", "QPE", "DEM")]
