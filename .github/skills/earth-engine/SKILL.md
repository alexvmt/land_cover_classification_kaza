---
name: earth-engine
description: Earth Engine feature extraction, aggregation, export, and inference workflows.
---

# When To Use

Use this skill when:

- modifying Earth Engine workflows
- implementing feature extraction
- implementing cloud masking
- implementing temporal aggregation
- debugging inference mismatches
- exporting models to Earth Engine

# Highest Priority Constraints

- Preserve feature ordering.
- Preserve feature names.
- Preserve Earth Engine compatibility.

# Canonical Workflow

Sentinel-2 ImageCollection
→ cloud masking
→ quarterly median aggregation
→ feature extraction
→ local training
→ export
→ Earth Engine inference

# Default Strategy

Use quarterly median composites.

# Core Rules

- Keep computations server-side.
- Minimize `.getInfo()` usage.
- Keep schemas stable.
- Keep temporal aggregation deterministic.

# Anti-Patterns

- renamed features
- dynamic schemas
- excessive `.getInfo()`
- preprocessing unavailable in Earth Engine

# Debugging Workflow

1. Verify feature names.
2. Verify feature ordering.
3. Verify masking logic.
4. Verify aggregation logic.
5. Compare feature values.
