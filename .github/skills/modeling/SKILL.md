---
name: modeling-workflow
description: Local scikit-learn training, evaluation, and Optuna optimization workflows.
---

# When To Use

Use this skill when:
- implementing model training
- implementing Optuna optimization
- modifying evaluation workflows
- implementing preprocessing pipelines
- modifying train/test splitting

# When Not To Use

Do not use this skill for:
- Earth Engine feature extraction
- CRS debugging
- visualization-only tasks

# Highest Priority Constraints

- Use reproducible train/test splits.
- Use stratified validation.
- Preserve feature ordering.
- Prevent data leakage.

# Canonical Workflow

feature extraction
→ preprocessing
→ train/test split
→ Optuna optimization
→ cross-validation
→ holdout evaluation
→ Earth Engine-compatible export

# Preferred Metrics

Optimize for:
- macro F1
- weighted F1
- balanced accuracy

Do not optimize solely for overall accuracy.

# Core Rules

- Set random seeds explicitly.
- Keep preprocessing reproducible.
- Use Optuna for hyperparameter optimization.
- Use polars for large tabular transformations unless pandas compatibility is required.

# Notebook Rules

- Use notebooks for exploration only.
- Move reusable logic into scripts or reusable modules.
- Keep notebooks restart-safe.
- Avoid hidden execution-order dependencies.

# Testing Priorities

Prioritize tests for:
- preprocessing
- feature engineering
- CRS consistency
- train/test splitting
- evaluation metrics

# Anti-Patterns

- Do not introduce data leakage.
- Do not optimize directly on the test set.
- Do not duplicate preprocessing logic.
- Do not use nondeterministic preprocessing.

# Evaluation Workflow

1. Evaluate cross-validation performance.
2. Evaluate holdout test performance.
3. Inspect per-class metrics.
4. Compare CV and test gaps.
5. Validate minority-class behavior.
