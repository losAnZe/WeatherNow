from typing import Any

RANGES = {"iwv": (10, 60), "cape": (0, 4000), "cin": (0, 200), "convergence": (0, 100), "shear": (0, 50), "ctt_cooling": (0, 15), "rainfall": (0, 150), "elevation": (0, 4000), "slope": (0, 45), "drainage": (0, 1)}

def normalize(features: dict[str, float]) -> dict[str, float]:
    """Min-max normalize known input features to [0, 1] with bounded outputs."""
    return {key: max(0.0, min(1.0, (value - low) / (high - low))) for key, value in features.items() if key in RANGES for low, high in [RANGES[key]]}

def build_features(raw: dict[str, float]) -> dict[str, float]:
    aliases = {"cttChange": "ctt_cooling", "rainfall_intensity": "rainfall"}
    prepared = {aliases.get(key, key): float(value) for key, value in raw.items()}
    return normalize(prepared)
