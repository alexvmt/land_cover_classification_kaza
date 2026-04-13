# Land Cover Classification for KAZA in Collaboration with [WWF Space Science Germany](https://space-science.wwf.de/)

Monitoring the distribution and evolution of land cover for conservation is challenging and important, for instance in the context of human-wildlife conflict or sustainable agricultural practices. Publically available satellite imagery (e.g., Sentinel-2) and machine learning techniques (e.g., random forest) can be used to create accurate annual land cover maps that consitute the basis for further analysis and decision support for impact monitoring efforts on the ground.

This repository contains a set of Google Earth Engine (EE) scripts and Python scripts and notebooks that together constitute the prototype of an end-to-end pipeline for land cover classification. A key feature of this pipeline is that the final model is trained locally while inference (i. e. creation of land cover map) is done directly in EE, which makes the whole process flexible and efficient. Naturally, there are several limitations to this process: e.g., availability of models than can be trained locally using `scikit-learn` and then be directly used in EE for inference.

The example used here focusses on the [Kavango-Zambezi Transfrontier Conservation Area](https://space-science.wwf.de/KAZAStory/) in Southern Africa. But the scripts and notebooks can be adapted to be used mostly anywhere on the planet, given one has suitable labeled data for model training.

**Key features:**
- Scriptable preprocessing and feature engineering
- Modular hyperparameter optimization using Optuna
- Inference via Google Earth Engine for scalable deployment

## Setup

```bash
git clone git@github.com:alexvmt/land_cover_classification_kaza.git
cd land_cover_classification_kaza
uv sync
```

## Pipeline steps

1. **Data collection** – Extract raw bands using `scripts/raw_data.js` in EE Code Editor
2. **Data preparation** – Process and split data using `scripts/prepare_data.py`
3. **Model optimization** – Tune hyperparameters using `scripts/optimize_model.py`
4. **Model export** – Export sklearn classifier to EE using `notebooks/export_model.ipynb`
5. **Inference** – Generate land cover map using `scripts/classified_image.js` in EE Code Editor

## Example land cover map

See below a section from an examplary land cover map for 2023 (Binga, Zimbabwe),
created using a random forest with default hyperparameters and quarterly raw bands as features.

![example land cover map](results/example_land_cover_map.png 'example land cover map')

## Modeling experiments

Experiments use random forest classifiers trained on quarterly Sentinel-2 raw bands and spectral indices. The dataset consists of ~3,303 training samples and 78,323 test samples. Hyperparameter optimization uses Optuna with 10-fold stratified cross-validation. Using a more fine-grained temporal resolution is possible but leads to less data for certain dates and areas because of pronounced cloud cover during the rainy season.

**Performance comparison:**

| Model | Accuracy | Precision | Recall | F1 Score | CV F1 Mean |
|-------|----------|-----------|--------|----------|------------|
| Default | 0.9325 | 0.7893 | 0.9307 | 0.8380 | 0.9297 |
| Optimized | 0.9313 | 0.7918 | 0.9292 | 0.8402 | 0.9242 |

The optimized model achieved marginally higher test F1 score (+0.22%) at the cost of increased complexity. Both models show strong performance with F1 ≥ 0.84 on the test set.

It is also noteworthy that the models don't perform equally well for all classes:

- F1 >= 0.9: water, cropland, forest and wetland
- F1 < 0.9 and F1 >= 0.8: built up, grass and shrub
- F1 < 0.8: bare

**Key observations:**
- Quarterly temporal resolution captures seasonal variability effectively
- High recall (~0.93) indicates the model correctly identifies most land cover areas
- Precision (~0.79) reflects class imbalance; some misclassification between similar classes (e.g., wetland vs. water)
- CV F1 (~0.93) vs. test F1 (~0.84) suggests mild overfitting, potentially mitigable with additional training data or regularization

## Feature importances

Feature importances from the optimized model reveal which Sentinel-2 bands and indices are most predictive for land cover classification.

![feature importances](results/feature_importances.png 'feature importances')

## Potential improvements

- Increase training sample size (especially underrepresented classes)
- Additional temporal features (e.g., NDVI slope, phenological metrics)
- Feature selection
- Experiment tracking using MLflow or Weights & Biases
