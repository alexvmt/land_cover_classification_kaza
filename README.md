# Land Cover Classification for KAZA in Collaboration with WWF Space Science Germany

## Setup

Clone repository and create directory structure.

`git clone git@github.com:alexvmt/land_cover_classification_kaza.git`

`cd land_cover_classification_kaza`

`mkdir data`

`mkdir models`

Upload to Google Drive and use with Google Colab.

## Steps

1. Get raw data using `raw_data.js` in Google Earth Engine Code Editor
2. Create train and test set using `train_and_test_set.ipynb` in Google Colab
3. *Optional: Run optimization using `optimization.ipynb` in Google Colab*
4. Train final model using `final_model.ipynb` in Google Colab
5. Create land cover map using `land_cover_map.ipynb` in Google Colab
6. Inspect created land cover map using `classified_image.js` in Google Earth Engine Code Editor

### Modeling experiments

| model        | features                          | set   | sample size | accuracy | precision | recall | f1     |
|--------------|-----------------------------------|-------|-------------|----------|-----------|--------|--------|
| rf default   | raw bands only                    | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | raw bands only                    | test  | 78321       | 0.8488   | 0.7012    | 0.8432 | 0.7276 |
| rf optimized | raw bands only                    | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | raw bands only                    | test  | 78321       | 0.8515   | 0.7075    | 0.8533 | 0.7372 |
| rf default   | raw bands and 4 indices           | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | raw bands and 4 indices           | test  | 78321       | 0.8467   | 0.6869    | 0.8296 | 0.7143 |
| rf optimized | raw bands and 4 indices           | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | raw bands and 4 indices           | test  | 78321       | 0.8504   | 0.6933    | 0.8495 | 0.7256 |
| rf default   | quarterly raw bands               | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | quarterly raw bands               | test  | 78321       | 0.8880   | 0.7060    | 0.8964 | 0.7540 |
| rf optimized | quarterly raw bands               | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | quarterly raw bands               | test  | 78321       | 0.8942   | 0.7145    | 0.9053 | 0.7647 |
| rf default   | quarterly raw bands and 4 indices | train | 3305        | 1        | 1         | 1      | 1      |
| rf default   | quarterly raw bands and 4 indices | test  | 78321       | 0.8895   | 0.7270    | 0.8910 | 0.7598 |
| rf optimized | quarterly raw bands and 4 indices | train | 3305        | 1        | 1         | 1      | 1      |
| rf optimized | quarterly raw bands and 4 indices | test  | 78321       | 0.8979   | 0.7383    | 0.9031 | 0.7793 |

### Example land cover map

![example land cover map](example_land_cover_map.png 'example land cover map')
