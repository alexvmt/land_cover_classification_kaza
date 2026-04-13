---
name: workspace-instructions
description: "Always follow Python, data science, and remote sensing best practices in this land cover classification project."
---

# Workspace Instructions for Land Cover Classification Project

## Python Best Practices and Standards
- Adhere to PEP 8 style guidelines for code formatting, including line length (100 characters), indentation (4 spaces), and naming conventions.
- Use type hints for function parameters and return values to improve code readability and enable static type checking.
- Include comprehensive docstrings for all public functions, classes, and modules using the Google or NumPy style (e.g., describe parameters, returns, and examples).
- Write clean, readable code with meaningful variable and function names; avoid abbreviations unless widely understood.
- Handle exceptions appropriately and use logging instead of print statements for debugging and monitoring.
- Prefer list comprehensions and generator expressions over explicit loops where they improve readability.
- Use virtual environments to manage dependencies and ensure reproducibility; uv in this case.

## Data Science Best Practices and Standards
- Prioritize data quality: Always perform exploratory data analysis (EDA) to understand distributions, missing values, and outliers before modeling.
- Ensure reproducibility by using random seeds for stochastic processes and documenting all preprocessing steps.
- Follow the CRISP-DM or similar methodology: Define clear problem statements, collect and clean data, engineer features, select and train models, evaluate performance, and deploy responsibly.
- Use appropriate metrics for evaluation (e.g., accuracy, precision, recall, F1-score, confusion matrix) and consider class imbalance in land cover classification tasks.
- Implement cross-validation to assess model generalization and avoid overfitting.
- Document data sources, transformations, and assumptions in notebooks or scripts for transparency.
- Version models and experiments using Weights and Biases (wandb).

## Remote Sensing Best Practices and Standards
- Handle geospatial data correctly: Use appropriate coordinate reference systems (CRS) and ensure consistent projections (e.g., WGS84 for global data, UTM for local analysis).
- Validate satellite imagery quality: Check for cloud cover, atmospheric corrections, and sensor calibration before analysis.
- Use established libraries like rasterio, geopandas, or GDAL for geospatial operations to ensure accuracy and efficiency.
- Consider spatial resolution, temporal frequency, and spectral bands when selecting data sources for land cover mapping.
- Implement proper masking for no-data values, water bodies, or irrelevant features in classification tasks.
- Validate classification results against ground truth data and use techniques like accuracy assessment polygons.
- Optimize for computational efficiency: Use parallel processing or cloud computing (e.g., Google Earth Engine) for large-scale remote sensing data.

## Additional Best Practices
- Maintain version control with Git: Commit frequently, use descriptive commit messages, and follow branching strategies (e.g., feature branches).
- Write unit tests for critical functions using pytest to ensure code reliability.
- Use Jupyter notebooks for exploratory analysis but convert key logic to reusable scripts or modules.
- Document the project thoroughly: Include a README.md with setup instructions, data descriptions, and usage examples.
- Prioritize ethical AI: Ensure models are unbiased, explainable, and do not perpetuate harm (e.g., consider environmental impact in land cover changes).
- Optimize performance: Profile code for bottlenecks and use efficient data structures (e.g., polars DataFrames for tabular data, NumPy arrays for numerical computations).
- Collaborate effectively: Use clear comments in code and maintain a project structure that separates data, models, scripts, and results.
