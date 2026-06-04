# Repository Overview

This repository implements a land cover classification pipeline for the
Kavango-Zambezi Transfrontier Conservation Area (KAZA).

Primary technologies:

- Google Earth Engine
- scikit-learn
- Optuna
- polars
- geopandas

Canonical workflow:

Sentinel-2
→ Earth Engine feature extraction
→ local model training
→ Earth Engine-compatible export
→ Earth Engine inference

# Repository Invariants

- Final inference runs inside Google Earth Engine.
- Earth Engine band names must match training features.
- Feature ordering must remain stable.
- Quarterly aggregation is the default temporal strategy.
- Macro F1 is the primary evaluation metric.
- Validation must be stratified.

# Repository Structure

- `scripts/` → executable workflows
- `notebooks/` → experimentation and exports
- `tests/` → automated validation
- `results/` → generated artifacts

See `.github/skills/` for workflow-specific guidance.
