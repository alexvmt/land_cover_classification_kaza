# Repository Overview

This repository implements a land cover classification pipeline for the
Kavango-Zambezi Transfrontier Conservation Area (KAZA).

Canonical workflow:
1. Sentinel-2 feature extraction in Google Earth Engine
2. Local preprocessing and scikit-learn training
3. Earth Engine-compatible model export
4. Final inference in Google Earth Engine

# Highest Priority Constraints

- Final inference must run inside Google Earth Engine.
- Earth Engine band names must exactly match training features.
- Feature ordering must remain identical between training and inference.
- Quarterly aggregation is the default temporal strategy.
- Macro F1 is the primary evaluation metric.
- Validation must be stratified.
- Reusable logic must not remain notebook-only.

# Repository Structure

- `scripts/` → executable pipeline steps
- `notebooks/` → exploration and export workflows
- `results/` → generated artifacts
- `tests/` → pytest tests

# Anti-Patterns

- Do not rename exported features after training.
- Do not use preprocessing unavailable in Earth Engine.
- Do not duplicate preprocessing logic across notebooks and scripts.
- Do not hardcode CRS assumptions.
- Do not use large `.getInfo()` calls in Earth Engine workflows.

# Tooling

Before committing changes:

```bash
ruff check .
ruff format .
ty check
pytest
```

See `.github/skills/` for workflow-specific guidance.
