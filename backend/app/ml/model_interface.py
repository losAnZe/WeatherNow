from abc import ABC, abstractmethod
from typing import Any

class NowcastingModel(ABC):
    """Adapter contract for demo or future trained multi-task models."""
    @abstractmethod
    def predict(self, atmospheric_grid: list[dict[str, float]], terrain_grid: list[dict[str, float]]) -> list[dict[str, float]]: ...

class FutureTrainedModel(NowcastingModel):
    """Placeholder: load validated model weights and inference runtime here."""
    def predict(self, atmospheric_grid: list[dict[str, float]], terrain_grid: list[dict[str, float]]) -> list[dict[str, float]]:
        raise NotImplementedError("Connect a trained model and real-data validation before enabling this provider.")
