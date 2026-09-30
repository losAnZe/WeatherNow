from .model_interface import NowcastingModel
from .feature_pipeline import build_features

WEIGHTS = {"thunderstorm": {"iwv": .17, "cape": .24, "cin": -.12, "convergence": .20, "shear": .10, "ctt_cooling": .17}, "cloudburst": {"iwv": .24, "cape": .13, "convergence": .13, "ctt_cooling": .22, "rainfall": .28}, "flash_flood": {"rainfall": .38, "cloudburst": .24, "elevation": .09, "slope": .10, "drainage": .19}}

class DemoModel(NowcastingModel):
    """Deterministic transparent scoring model; values are illustrative, not calibrated."""
    def predict(self, atmospheric_grid: list[dict[str, float]], terrain_grid: list[dict[str, float]]) -> list[dict[str, float]]:
        results = []
        for index, raw in enumerate(atmospheric_grid):
            features = build_features(raw)
            terrain = build_features(terrain_grid[index] if index < len(terrain_grid) else {})
            features.update(terrain)
            outputs = {}
            for head, weights in WEIGHTS.items():
                score = sum((1 - features.get(name, 0)) * abs(weight) if weight < 0 else features.get(name, 0) * weight for name, weight in weights.items())
                total = sum(abs(weight) for weight in weights.values())
                outputs[head] = round(max(0, min(100, score / total * 100)))
            results.append(outputs)
        return results
