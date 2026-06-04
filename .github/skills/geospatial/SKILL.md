---
name: geospatial
description: Geospatial processing and remote sensing workflows.
---

# When To Use

Use this skill when:

- processing raster data
- handling CRS transformations
- creating remote sensing features
- implementing spatial validation

# Highest Priority Constraints

- Preserve CRS consistency.
- Preserve raster alignment.
- Handle no-data explicitly.

# Default Feature Strategy

Use:

- Sentinel-2 bands
- NDVI
- NDWI
- EVI
- quarterly temporal aggregation
- temporal medians

# Core Rules

- Use EPSG:4326 unless another CRS is required.
- Preserve CRS metadata.
- Avoid pixel-wise Python loops.
- Prefer vectorized operations.

# Evaluation Rules

- Report macro F1.
- Inspect per-class metrics.
- Evaluate minority classes explicitly.

# Anti-Patterns

- mixed CRS
- mixed spatial resolutions
- implicit no-data handling
- changing feature schemas
