from .demo_model import DemoModel

class InferenceService:
    def __init__(self) -> None:
        self.model = DemoModel()
    def run(self, atmospheric_grid: list[dict[str, float]], terrain_grid: list[dict[str, float]]) -> dict[str, object]:
        return {"dataSource": "SIMULATED_DEMO", "model": "Deterministic prototype scoring rules", "predictions": self.model.predict(atmospheric_grid, terrain_grid)}
