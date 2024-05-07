# Land Cover Classification for KAZA in Collaboration with [WWF Space Science Germany](https://space-science.wwf.de/)

Monitoring the distribution and evolution of land cover for conservation is challenging and important,
for instance in the context of human-wildlife conflict or sustainable agricultural practices.
Publically available satellite imagery (e. g. Sentinel-2) and machine learning techniques (e. g. random forest) can be used 
to create accurate annual land cover maps that consitute the basis for further analysis
and decision support for impact monitoring efforts on the ground.

This repository contains a set of Google Earth Engine (EE) scripts and Google Colab (Colab) notebooks
that together constitute the prototype of an end-to-end pipeline for land cover classification.
A key feature of this pipeline is that the final model is trained locally in Colab
while inference (i. e. creation of land cover map) is done directly in EE,
which makes the whole process flexible and efficient.
Naturally, there are several limitations to this process,
e. g. availability of models than can be trained locally using `scikit-learn` and
then be directly used in EE for inference.

The example used here focusses on the [Kavango-Zambezi Transfrontier Conservation Area](https://space-science.wwf.de/KAZAStory/) in Southern Africa.
But the scripts and notebooks can be adapted to be used mostly anywhere on the planet,
given one has suitable labeled data for model training.

## Setup

Clone the repository and create the directory structure.

```
git clone git@github.com:alexvmt/land_cover_classification_kaza.git
cd land_cover_classification_kaza
mkdir data
mkdir models
```

Upload the repository to Google Drive and use the notebooks with Colab.

## Steps

1. Get raw data using `raw_data.js` in EE Code Editor
2. Create train and test set using `train_and_test_set.ipynb` in Colab
3. *Optional: Run optimization with `auto-sklearn` using `optimization.ipynb` in Colab*
4. Train final model using `final_model.ipynb` in Colab
5. Create land cover map using `land_cover_map.ipynb` in Colab
6. Inspect created land cover map using `classified_image.js` in EE Code Editor

## Example land cover map

See below a section from an examplary land cover map for 2023 (Binga, Zimbabwe),
created using a random forest with default hyperparameters and quarterly raw bands as features.

![example land cover map](example_land_cover_map.png 'example land cover map')

## Modeling experiments

The modeling experiments have been conducted using random forest only since it is not only a popular choice for the task at hand
but also since there is no functionality to train a model locally and then deploy it to EE for most other models available in EE.

The experiments compare performance in terms of standard classification metrics
for random forest with default hyperparameters and random forest with optimized hyperparameters (found using `auto-sklearn`).

Besides, different configurations of the data structure and sets of features are also compared:
- annual, seasonal (rainy and dry) and quarterly data
- raw bands and standard remote sensing indices (e. g. NDVI, NDWI, SAVI, EVI)

It is possible to create an even more granular monthly time series of the data, but doing so results in a reduced sample size.
This is due to the fact that there is pronounced cloud cover during the rainy season which in turn leads to less data for certain dates and areas.

Due to severe class imbalance the training data is rather small. The test data has not been balanced.

The table below shows the experiments' results. The key observations are:
- Focussing on the test set, performance tends to increase with the granularity of the data.
- The optimized model tends to yield only minor improvements at the cost of increased complexity and effort.
- Adding indices doesn't tend to improve performance.
- The models classify the training data perfectly, leading to a fairly large gap compared to the test set.
This could be due to overfitting which could potentially be alleviated using more training data, using less features, reducing model complexity or using regularization.

It is also noteworthy that the models don't perform equally well for all classes:
- F1 >= 0.9: water, cropland, forest and wetland
- F1 < 0.9 and F1 >= 0.8: built up, grass and shrub
- F1 < 0.8: bare
In some case there is also significant confusion between classes.

| model        | features                        | set   | sample size | accuracy | precision | recall | f1     |
|--------------|---------------------------------|-------|-------------|----------|-----------|--------|--------|
| rf default   | raw bands only                  | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | raw bands only                  | test  | 78321       | 0.8488   | 0.7012    | 0.8432 | 0.7276 |
| rf optimized | raw bands only                  | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | raw bands only                  | test  | 78321       | 0.8515   | 0.7075    | 0.8533 | 0.7372 |
| rf default   | raw bands and indices           | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | raw bands and indices           | test  | 78321       | 0.8467   | 0.6869    | 0.8296 | 0.7143 |
| rf optimized | raw bands and indices           | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | raw bands and indices           | test  | 78321       | 0.8504   | 0.6933    | 0.8495 | 0.7256 |
| rf default   | seasonal raw bands              | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | seasonal raw bands              | test  | 78321       | 0.888    | 0.706     | 0.8964 | 0.754  |
| rf optimized | seasonal raw bands              | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | seasonal raw bands              | test  | 78321       | 0.8942   | 0.7145    | 0.9053 | 0.7647 |
| rf default   | seasonal raw bands and indices  | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | seasonal raw bands and indices  | test  | 78321       | 0.8895   | 0.727     | 0.891  | 0.7598 |
| rf optimized | seasonal raw bands and indices  | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | seasonal raw bands and indices  | test  | 78321       | 0.8979   | 0.7383    | 0.9031 | 0.7793 |
| rf default   | quarterly raw bands             | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | quarterly raw bands             | test  | 78321       | 0.9295   | 0.7882    | 0.9352 | 0.8295 |
| rf optimized | quarterly raw bands             | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | quarterly raw bands             | test  | 78321       | 0.9356   | 0.8189    | 0.9398 | 0.8565 |
| rf default   | quarterly raw bands and indices | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | quarterly raw bands and indices | test  | 78321       | 0.9303   | 0.772     | 0.9322 | 0.82   |
| rf optimized | quarterly raw bands and indices | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | quarterly raw bands and indices | test  | 78321       | 0.9355   | 0.81      | 0.9429 | 0.8527 |

## Feature importances

Below is a comparison of feature importances for the default and the optimized random forest, using quarterly data and raw bands only as features.
The notebook `final_model.ipynb` also contains permutation importances for the train and test set.

![compared feature importances](compared_feature_importances.png 'compared feature importances')

## Summary and open questions

The pipeline is set up and working, can be transferred to other use cases and the first results look promising.
It surely can be improved, e. g. in terms of usability and efficiency.
And there are open questions, such as:
- How can the amount of data, especially for certain rare classes, be increased?
- Can the data structure be improved?
- Why don't the indices improve performance as expected? Which other features can be added?
- Is an efficient feature selection process necessary?
- Why doesn't the optimization yield significant performance improvements?
- How to overcome overfitting?
- The model doesn't seem to ever predict water but only wetland. What can be done here? Is this even an issue?
