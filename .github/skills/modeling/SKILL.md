---
name: modeling
description: Local scikit-learn training and Optuna optimization workflows.
---

# When To Use

Use this skill when:

- implementing training workflows
- implementing Optuna studies
- modifying evaluation pipelines
- modifying preprocessing

# Highest Priority Constraints

- Prevent data leakage.
- Preserve feature ordering.
- Use stratified validation.
- Keep preprocessing reproducible.

# Canonical Workflow

features
→ preprocessing
→ train/test split
→ Optuna optimization
→ cross-validation
→ holdout evaluation
→ export

# Preferred Metrics

Optimize for:

- macro F1
- weighted F1
- balanced accuracy

# Core Rules

- Set random seeds.
- Use Optuna.
- Use polars for large tabular transformations.
- Keep feature schemas stable.

# Anti-Patterns

- optimizing on test data
- nondeterministic preprocessing
- duplicated preprocessing
- feature schema drift

# Evaluation Workflow

1. Evaluate CV performance.
2. Evaluate holdout performance.
3. Inspect per-class metrics.
4. Compare CV/test gaps.
5. Review minority-class performance.
