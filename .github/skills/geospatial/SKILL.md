---
name: geospatial-workflow
description: Geospatial processing and remote sensing workflows for Sentinel-2 land cover classification.
---

# When To Use

Use this skill when:
- working with CRS transformations
- implementing raster preprocessing
- implementing feature engineering
- handling geospatial datasets
- creating remote sensing features

# When Not To Use

Do not use this skill for:
- Optuna optimization logic
- Earth Engine export debugging
- generic Python refactoring

# Highest Priority Constraints

- Preserve CRS consistency.
- Preserve raster alignment and resolution.
- Handle no-data values explicitly.
- Keep preprocessing deterministic.

# Core Rules

- Use EPSG:4326 unless another CRS is explicitly required.
- Ensure all geometries share the same CRS before spatial operations.
- Preserve CRS metadata during transformations.
- Prefer vectorized geospatial operations.
- Avoid pixel-wise Python loops.

# Canonical Feature Strategy

Use:
- Sentinel-2 raw bands
- vegetation indices
- water indices
- quarterly temporal aggregation
- temporal medians

# Common Indices

- NDVI
- NDWI
- EVI
- SAVI

# Evaluation Rules

- Report macro F1.
- Evaluate minority land cover classes explicitly.
- Inspect per-class metrics.

# Anti-Patterns

- Do not mix incompatible spatial resolutions.
- Do not rely on implicit CRS assumptions.
- Do not ignore cloud contamination.
- Do not change feature schemas between experiments.
