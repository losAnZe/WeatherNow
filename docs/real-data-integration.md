# Real-data and trained-model integration

This describes integration seams only. No external weather endpoint or dataset is wired into the prototype.

1. Implement adapters for satellite imagery (INSAT), atmospheric analysis (IMDAA), precipitation (QPE), and terrain (DEM). Include credentials, licensing, product/version, projection, unit metadata and provider terms in configuration.
2. Validate provenance, timestamps, missing-data masks, georeferencing, units and quality flags. Align grids and time windows before feature assembly.
3. Extend `feature_pipeline.py` with tested/versioned transformations, normalization metadata and missing-value policy. Do not fit normalization on evaluation or inference data.
4. Implement a trained PyTorch model behind `NowcastingModel`. A future multi-task model may use a shared spatial-temporal encoder and calibrated thunderstorm, cloudburst and flash-flood heads. Persist model version, input schema, weights, thresholds and inference metadata.
5. Evaluate event-based splits, lead-time and spatial metrics, probability calibration, class imbalance, regional performance, uncertainty and false alarms. Obtain domain review before any operational use.
6. Publish raster/vector predictions with CRS, valid time and provenance. Use approved authoritative sources for impact data; keep freshness, quality and outages visible.
7. Review thresholds, wording and escalation process with responsible authorities. Prototype alert wording is not public safety guidance.

## Prototype scoring

`backend/app/ml/demo_model.py` contains deterministic bounded feature scores for interaction only. `backend/app/services/alerts.py` holds demonstration thresholds. Neither is validated operational logic.
