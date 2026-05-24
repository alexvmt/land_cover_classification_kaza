---
name: earth-engine-workflow
description: Earth Engine feature extraction and inference workflows for Sentinel-2 land cover classification.
---

# When To Use

Use this skill when:
- modifying Earth Engine workflows
- implementing Sentinel-2 feature extraction
- implementing temporal aggregation
- debugging Earth Engine inference mismatches
- exporting models to Earth Engine-compatible formats

# When Not To Use

Do not use this skill for:
- generic Python refactoring
- local-only sklearn experimentation
- visualization-only tasks

# Highest Priority Constraints

- Preserve exact feature names.
- Preserve exact feature ordering.
- Maintain Earth Engine inference compatibility.
- Keep computations server-side whenever possible.

# Canonical Workflow

Sentinel-2 ImageCollection
→ cloud masking
→ quarterly median aggregation
→ feature extraction
→ local scikit-learn training
→ Earth Engine-compatible export
→ Earth Engine inference

# Default Temporal Strategy

Use quarterly median composites unless explicitly experimenting with another strategy.

# Core Rules

- Minimize `.getInfo()` usage.
- Keep temporal aggregation deterministic.
- Keep feature schemas stable across experiments.
- Ensure Earth Engine band names exactly match training features.

# Preferred Models

Preferred estimators:
- RandomForestClassifier
- CART-style tree models

Avoid:
- unsupported neural network architectures
- preprocessing unavailable in Earth Engine
- dynamically changing feature schemas

# Common Failure Sources

- mismatched feature ordering
- renamed features
- inconsistent masking
- missing bands
- inconsistent temporal aggregation

# Debugging Workflow

1. Verify feature ordering.
2. Verify feature names.
3. Verify masking logic.
4. Verify temporal aggregation.
5. Compare intermediate feature values.
