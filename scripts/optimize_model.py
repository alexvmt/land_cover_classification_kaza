#!/usr/bin/env python3
"""Script to optimize Random Forest hyperparameters using Optuna."""

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from model_optimization import (
    FeatureImportanceExporter,
    ModelEvaluator,
    ModelTrainer,
    OptunaSampler,
    load_data_from_csv,
)


def main():
    """Main function to run model optimization."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Define paths
    data_dir = Path(__file__).parent.parent / "data"
    train_csv = data_dir / "train.csv"
    test_csv = data_dir / "test.csv"

    models_dir = Path(__file__).parent.parent / "models"
    media_dir = Path(__file__).parent.parent / "media"
    results_dir = Path(__file__).parent.parent / "results"

    # Check if input exists
    if not train_csv.exists() or not test_csv.exists():
        logger.error("Data files not found")
        sys.exit(1)

    logger.info("=" * 80)
    logger.info("STARTING MODEL OPTIMIZATION WORKFLOW")
    logger.info("=" * 80)

    # Load data
    logger.info("Loading data...")
    X_train, y_train, X_test, y_test = load_data_from_csv(train_csv, test_csv)
    logger.info(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

    # Run Optuna hyperparameter search
    logger.info("\nRunning Optuna hyperparameter search...")
    sampler = OptunaSampler(
        X_train=X_train,
        y_train=y_train,
        cv_folds=10,
        random_state=42,
    )
    sampler.optimize(n_trials=10)
    best_hyperparams = sampler.get_best_hyperparams()
    logger.info(f"Best hyperparameters: {best_hyperparams}")

    # Train optimized model
    logger.info("\nTraining optimized model...")
    trainer = ModelTrainer(random_state=42)
    optimized_model = trainer.train(X_train, y_train, best_hyperparams)

    # Train default model for comparison
    logger.info("Training default model...")
    default_hyperparams = {
        "n_estimators": 100,
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
        "random_state": 42,
        "n_jobs": -1,
    }
    default_model = trainer.train(X_train, y_train, default_hyperparams)

    # Save optimized model
    logger.info("\nSaving optimized model...")
    model_path = models_dir / "optimized_rf_model.joblib"
    trainer.save_model(optimized_model, model_path)

    # Export feature importances
    logger.info("Exporting feature importances...")
    feature_names = X_train.columns.tolist()
    FeatureImportanceExporter.export(optimized_model, feature_names, media_dir)

    # Evaluate and compare models
    logger.info("Evaluating and comparing models...")
    evaluator = ModelEvaluator(cv_folds=10, random_state=42)
    comparison_df = evaluator.compare_models(
        default_model,
        optimized_model,
        best_hyperparams,
        X_train,
        y_train,
        X_test,
        y_test,
        output_path=results_dir / "optimization_comparison.csv",
    )

    logger.info("\n" + "=" * 80)
    logger.info("MODEL OPTIMIZATION WORKFLOW COMPLETE")
    logger.info("=" * 80)
    logger.info("\nResults:")
    logger.info(comparison_df.to_string())
    logger.info("\nOutputs saved to:")
    logger.info(f"  - Model: {model_path}")
    logger.info(f"  - Feature importances: {media_dir}/")
    logger.info(f"  - Comparison: {results_dir}/optimization_comparison.csv")


if __name__ == "__main__":
    main()
