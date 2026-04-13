"""
Model optimization module for land cover classification using Optuna and Random Forest.

This module provides focused classes for hyperparameter optimization, model training,
evaluation, and result persistence.
"""

import json
import logging
from pathlib import Path
from typing import Optional

import joblib
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
import polars as pl
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate

logger = logging.getLogger(__name__)


def load_data_from_csv(
    train_path: Path | str,
    test_path: Path | str,
    target_column: str = "Landcover",
    drop_columns: Optional[list[str]] = None,
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Load and prepare data from CSV files.

    Converts Polars DataFrames to pandas for sklearn compatibility.

    Args:
        train_path: Path to training CSV.
        test_path: Path to test CSV.
        target_column: Name of target column. Defaults to "Landcover".
        drop_columns: Columns to drop. Defaults to ["LC_Nr", "LC_Out"].

    Returns:
        Tuple of (X_train, y_train, X_test, y_test) as pandas objects.
    """
    if drop_columns is None:
        drop_columns = ["LC_Nr", "LC_Out"]

    logger.info(f"Loading training data from {train_path}")
    train_df = pl.read_csv(train_path)
    train_df = train_df.drop([c for c in drop_columns if c in train_df.columns])

    y_train = train_df[target_column].to_pandas()
    X_train = train_df.drop(target_column).to_pandas()

    logger.info(f"Loading test data from {test_path}")
    test_df = pl.read_csv(test_path)
    test_df = test_df.drop([c for c in drop_columns if c in test_df.columns])

    y_test = test_df[target_column].to_pandas()
    X_test = test_df.drop(target_column).to_pandas()

    # Handle infinities by replacing with NaN
    X_train = X_train.replace([np.inf, -np.inf], np.nan)
    X_test = X_test.replace([np.inf, -np.inf], np.nan)

    # Drop rows with any missing values (NaN or inf)
    initial_train_rows = len(X_train)
    X_train, y_train = X_train.dropna(how="any").align(y_train, join="inner", axis=0)
    dropped_train = initial_train_rows - len(X_train)
    if dropped_train > 0:
        logger.warning(f"Dropped {dropped_train} training rows with NaN/inf values")

    initial_test_rows = len(X_test)
    X_test, y_test = X_test.dropna(how="any").align(y_test, join="inner", axis=0)
    dropped_test = initial_test_rows - len(X_test)
    if dropped_test > 0:
        logger.warning(f"Dropped {dropped_test} test rows with NaN/inf values")

    logger.info(f"Loaded training: {X_train.shape}, Test: {X_test.shape}")

    return X_train, y_train, X_test, y_test


class OptunaSampler:
    """
    Manages Optuna hyperparameter search for Random Forest.

    Handles trial creation, objective function definition, and study optimization.
    """

    def __init__(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        cv_folds: int = 10,
        random_state: int = 42,
    ):
        """
        Initialize OptunaSampler.

        Args:
            X_train: Training features.
            y_train: Training target.
            cv_folds: Number of cross-validation folds. Defaults to 10.
            random_state: Random seed. Defaults to 42.
        """
        self.X_train = X_train
        self.y_train = y_train
        self.cv_folds = cv_folds
        self.random_state = random_state
        self.study = None
        self.best_trial = None

        logger.info(f"Initialized OptunaSampler with {cv_folds}-fold CV")

    def _get_hyperparams(self, trial: optuna.trial.Trial) -> dict:
        """
        Suggest hyperparameters for Random Forest.

        Args:
            trial: Optuna trial object.

        Returns:
            Dictionary of hyperparameters.
        """
        return {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500),
            "max_depth": trial.suggest_int("max_depth", 5, 50),
            "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
            "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2"]),
            "random_state": self.random_state,
            "n_jobs": -1,
        }

    def objective(self, trial: optuna.trial.Trial) -> float:
        """
        Optuna objective function for hyperparameter optimization.

        Evaluates a trial using stratified k-fold cross-validation with F1 macro scoring.

        Args:
            trial: Optuna trial object.

        Returns:
            Mean F1 macro score across cross-validation folds.
        """
        try:
            hyperparams = self._get_hyperparams(trial)

            # Define cross-validation strategy
            cv = StratifiedKFold(
                n_splits=self.cv_folds,
                shuffle=True,
                random_state=self.random_state,
            )

            # Create RF model
            rf = RandomForestClassifier(**hyperparams)

            # Perform cross-validation with F1 macro scoring
            cv_results = cross_validate(
                rf,
                self.X_train,
                self.y_train,
                cv=cv,
                scoring="f1_macro",
                n_jobs=-1,
            )

            f1_mean = cv_results["test_score"].mean()

            # Log trial progress
            trial_num = trial.number
            logger.info(
                f"Trial {trial_num}: F1 (CV mean)={f1_mean:.4f}, "
                f"n_est={hyperparams['n_estimators']}, "
                f"max_depth={hyperparams['max_depth']}"
            )

            return f1_mean

        except Exception as e:
            logger.warning(f"Trial {trial.number} failed: {str(e)}")
            return 0.0

    def optimize(self, n_trials: int) -> None:
        """
        Run Optuna optimization for n_trials trials.

        Args:
            n_trials: Number of trials to run.
        """
        logger.info(f"Starting optimization with {n_trials} trials...")

        # Create study with TPE sampler
        sampler = TPESampler(seed=self.random_state)
        self.study = optuna.create_study(
            direction="maximize",
            sampler=sampler,
        )

        # Optimize
        self.study.optimize(self.objective, n_trials=n_trials, show_progress_bar=False)

        # Get best trial
        self.best_trial = self.study.best_trial

        logger.info(f"Optimization complete. Best trial: {self.best_trial.number}")
        logger.info(f"Best F1 (CV mean): {self.best_trial.value:.4f}")
        logger.info(f"Best hyperparameters: {json.dumps(self.best_trial.params, indent=2)}")

    def get_best_hyperparams(self) -> dict:
        """
        Extract hyperparameters from best trial.

        Returns:
            Dictionary of best hyperparameters.
        """
        if self.best_trial is None:
            raise ValueError("No best trial found. Run optimize() first.")

        trial_params = self.best_trial.params
        return {
            "n_estimators": trial_params["n_estimators"],
            "max_depth": trial_params["max_depth"],
            "min_samples_split": trial_params["min_samples_split"],
            "min_samples_leaf": trial_params["min_samples_leaf"],
            "max_features": trial_params["max_features"],
            "random_state": self.random_state,
            "n_jobs": -1,
        }


class ModelTrainer:
    """
    Trains Random Forest models with specified hyperparameters.
    """

    def __init__(self, random_state: int = 42):
        """
        Initialize ModelTrainer.

        Args:
            random_state: Random seed. Defaults to 42.
        """
        self.random_state = random_state

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        hyperparams: dict,
    ) -> RandomForestClassifier:
        """
        Train Random Forest with given hyperparameters.

        Args:
            X_train: Training features.
            y_train: Training target.
            hyperparams: Dictionary of hyperparameters.

        Returns:
            Trained RandomForestClassifier.
        """
        rf = RandomForestClassifier(**hyperparams)
        rf.fit(X_train, y_train)
        logger.info(f"Trained RF with {rf.n_estimators} estimators, {rf.max_depth} max_depth")
        return rf

    def save_model(
        self,
        model: RandomForestClassifier,
        output_path: Path | str,
    ) -> None:
        """
        Save trained model to disk using joblib.

        Args:
            model: Trained RandomForestClassifier.
            output_path: Path to save model.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, output_path)
        logger.info(f"Model saved to {output_path}")


class ModelEvaluator:
    """
    Evaluates models and compares performance metrics.
    """

    def __init__(self, cv_folds: int = 10, random_state: int = 42):
        """
        Initialize ModelEvaluator.

        Args:
            cv_folds: Number of cross-validation folds. Defaults to 10.
            random_state: Random seed. Defaults to 42.
        """
        self.cv_folds = cv_folds
        self.random_state = random_state

    def evaluate_model(
        self,
        model: RandomForestClassifier,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        model_name: str = "Model",
    ) -> dict:
        """
        Evaluate model on both CV and test set.

        Args:
            model: Trained RandomForestClassifier.
            X_train: Training features.
            y_train: Training target.
            X_test: Test features.
            y_test: Test target.
            model_name: Name of model for logging.

        Returns:
            Dictionary of evaluation metrics.
        """
        # Train CV score
        cv = StratifiedKFold(
            n_splits=self.cv_folds,
            shuffle=True,
            random_state=self.random_state,
        )
        cv_results = cross_validate(
            model,
            X_train,
            y_train,
            cv=cv,
            scoring="f1_macro",
        )
        f1_cv_mean = cv_results["test_score"].mean()

        # Test set metrics
        y_pred = model.predict(X_test)
        f1_test = f1_score(y_test, y_pred, average="macro", zero_division=0)
        accuracy_test = accuracy_score(y_test, y_pred)
        precision_test = precision_score(y_test, y_pred, average="macro", zero_division=0)
        recall_test = recall_score(y_test, y_pred, average="macro", zero_division=0)

        logger.info(
            f"{model_name} - F1 (CV): {f1_cv_mean:.4f}, F1 (Test): {f1_test:.4f}, "
            f"Accuracy (Test): {accuracy_test:.4f}"
        )

        return {
            "Model": model_name,
            "F1_CV_Mean": f1_cv_mean,
            "F1_Test": f1_test,
            "Accuracy_Test": accuracy_test,
            "Precision_Test": precision_test,
            "Recall_Test": recall_test,
        }

    def compare_models(
        self,
        default_model: RandomForestClassifier,
        optimized_model: RandomForestClassifier,
        optimized_hyperparams: dict,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        output_path: Path | str = "results/optimization_comparison.csv",
    ) -> pd.DataFrame:
        """
        Train and compare default vs optimized models.

        Args:
            default_model: Model with default hyperparameters.
            optimized_model: Model with optimized hyperparameters.
            optimized_hyperparams: Hyperparameters of optimized model.
            X_train: Training features.
            y_train: Training target.
            X_test: Test features.
            y_test: Test target.
            output_path: Path to save comparison CSV.

        Returns:
            DataFrame with comparison results.
        """
        # Evaluate models
        default_results = self.evaluate_model(
            default_model,
            X_train,
            y_train,
            X_test,
            y_test,
            "Default",
        )
        optimized_results = self.evaluate_model(
            optimized_model,
            X_train,
            y_train,
            X_test,
            y_test,
            "Optimized",
        )

        # Add feature and hyperparameter info
        n_features = X_train.shape[1]
        default_results["Selected_Features_Count"] = n_features
        optimized_results["Selected_Features_Count"] = n_features
        default_results["Hyperparams_JSON"] = json.dumps({})
        optimized_results["Hyperparams_JSON"] = json.dumps(
            {k: str(v) for k, v in optimized_hyperparams.items()}
        )

        # Create comparison dataframe
        comparison_df = pd.DataFrame([default_results, optimized_results])

        # Save to CSV
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        comparison_df.to_csv(output_path, index=False)
        logger.info(f"Comparison results saved to {output_path}")

        return comparison_df


class FeatureImportanceExporter:
    """
    Exports feature importances as CSV and PNG visualization.
    """

    @staticmethod
    def export(
        model: RandomForestClassifier,
        feature_names: list[str],
        output_dir: Path | str = "media",
    ) -> None:
        """
        Export feature importances as CSV and PNG.

        Args:
            model: Trained RandomForestClassifier.
            feature_names: List of feature names.
            output_dir: Directory to save outputs. Defaults to "media".
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Get feature importances
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame(
            {
                "feature_name": feature_names,
                "importance_score": importances,
            }
        ).sort_values("importance_score", ascending=False)

        # Save CSV
        csv_path = output_dir / "feature_importances.csv"
        feature_importance_df.to_csv(csv_path, index=False)
        logger.info(f"Feature importances CSV saved to {csv_path}")

        # Save PNG (top-20 features)
        top_n = min(20, len(feature_importance_df))
        top_features = feature_importance_df.head(top_n)

        plt.figure(figsize=(10, 8))
        plt.barh(range(len(top_features)), top_features["importance_score"].values)
        plt.yticks(range(len(top_features)), top_features["feature_name"].values, fontsize=9)
        plt.xlabel("Importance Score", fontsize=11)
        plt.ylabel("Feature", fontsize=11)
        plt.title(
            f"Top {top_n} Feature Importances (Random Forest)", fontsize=12, fontweight="bold"
        )
        plt.tight_layout()

        png_path = output_dir / "feature_importances.png"
        plt.savefig(png_path, dpi=100, bbox_inches="tight")
        plt.close()
        logger.info(f"Feature importances PNG saved to {png_path}")
