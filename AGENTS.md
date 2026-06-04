# KAZA Agent Guide

This repository implements a land cover classification pipeline for the
Kavango-Zambezi Transfrontier Conservation Area (KAZA).

The repository combines:

- Google Earth Engine feature extraction
- local scikit-learn training
- Optuna hyperparameter optimization
- Earth Engine-compatible model export
- large-scale Earth Engine inference

# Primary Goal

Make the smallest change that correctly solves the requested task.

Preserve existing behavior unless explicitly instructed otherwise.

# Planning

Before making changes:

1. Identify affected pipeline stages.
2. Verify feature schema implications.
3. Verify Earth Engine compatibility implications.
4. Reuse existing project patterns.
5. Minimize affected files.

# Repository Workflow

Canonical workflow:

Sentinel-2 ImageCollection
→ cloud masking
→ quarterly aggregation
→ feature extraction
→ local preprocessing
→ model training
→ evaluation
→ Earth Engine-compatible export
→ Earth Engine inference

# Highest Priority Constraints

- Final inference must run inside Google Earth Engine.
- Feature ordering must remain stable.
- Feature names must remain stable.
- Earth Engine band names must match training features.
- Preprocessing must be reproducible in Earth Engine.
- Prevent data leakage.

# Feature Engineering Rules

Before modifying features:

1. Verify Earth Engine implementation exists.
2. Verify naming consistency.
3. Verify export compatibility.
4. Verify inference compatibility.

Never introduce features that cannot be reproduced during Earth Engine inference.

# Refactoring Rules

Prefer:

- extraction over rewriting
- incremental changes over redesigns
- existing repository patterns
- simple functions

Avoid:

- speculative abstractions
- framework-style architecture
- unnecessary classes
- giant utility modules

# Geospatial Safety Rules

- Preserve CRS metadata.
- Preserve raster alignment.
- Preserve spatial resolution assumptions.
- Handle no-data values explicitly.

# Modeling Safety Rules

- Use stratified validation.
- Preserve train/test separation.
- Preserve feature ordering.
- Report macro F1.
- Evaluate minority classes explicitly.

# Validation

Before finalizing changes:

```bash
ruff check .
ruff format .
ty check
pytest
```

If a command cannot be executed, explain why.

# Scope Control

Do not modify unrelated files.

Do not change hyperparameters unless requested.

Do not change feature schemas unless requested.

Do not rewrite working code without a clear reason.

Prefer small, reviewable diffs.
