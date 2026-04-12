"""
Unit tests for model_optimization module.

Tests cover individual classes for optimization, training, evaluation,
and feature importance export.
"""

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.model_optimization import (
    FeatureImportanceExporter,
    ModelEvaluator,
    ModelTrainer,
    OptunaSampler,
    load_data_from_csv,
)


@pytest.fixture
def sample_data():
    """Create small sample dataset for testing."""
    np.random.seed(42)

    # Create features: some bands and indices
    n_train_samples = 100
    n_test_samples = 100
    features_train = {
        "B2_Q1": np.random.randn(n_train_samples),
        "B2_Q2": np.random.randn(n_train_samples),
        "B3_Q1": np.random.randn(n_train_samples),
        "B3_Q2": np.random.randn(n_train_samples),
        "B4_Q1": np.random.randn(n_train_samples),
        "B4_Q2": np.random.randn(n_train_samples),
        "NDVI_Q1": np.random.randn(n_train_samples),
        "NDVI_Q2": np.random.randn(n_train_samples),
        "NDWI_MCF_Q1": np.random.randn(n_train_samples),
        "NDWI_MCF_Q2": np.random.randn(n_train_samples),
    }

    features_test = {
        "B2_Q1": np.random.randn(n_test_samples),
        "B2_Q2": np.random.randn(n_test_samples),
        "B3_Q1": np.random.randn(n_test_samples),
        "B3_Q2": np.random.randn(n_test_samples),
        "B4_Q1": np.random.randn(n_test_samples),
        "B4_Q2": np.random.randn(n_test_samples),
        "NDVI_Q1": np.random.randn(n_test_samples),
        "NDVI_Q2": np.random.randn(n_test_samples),
        "NDWI_MCF_Q1": np.random.randn(n_test_samples),
        "NDWI_MCF_Q2": np.random.randn(n_test_samples),
    }

    X_train = pd.DataFrame(features_train)
    X_test = pd.DataFrame(features_test)

    # Create target (imbalanced classes)
    y_train = np.random.choice([0, 1, 2], n_train_samples, p=[0.6, 0.3, 0.1])
    y_test = np.random.choice([0, 1, 2], n_test_samples, p=[0.6, 0.3, 0.1])

    return X_train, pd.Series(y_train), X_test, pd.Series(y_test)


class TestOptunaSampler:
    """Tests for OptunaSampler class."""

    def test_initialization(self, sample_data):
        """Test OptunaSampler initialization."""
        X_train, y_train, _, _ = sample_data

        sampler = OptunaSampler(X_train, y_train, cv_folds=5, random_state=42)

        assert sampler.cv_folds == 5
        assert sampler.random_state == 42
        assert sampler.study is None
        assert sampler.best_trial is None

    def test_objective_function(self, sample_data):
        """Test objective function works."""
        X_train, y_train, _, _ = sample_data

        sampler = OptunaSampler(X_train, y_train, cv_folds=3, random_state=42)

        # Create a mock trial
        class MockTrial:
            number = 0

            def suggest_int(self, name, low, high):
                return (low + high) // 2

            def suggest_categorical(self, name, choices):
                return choices[0]

        trial = MockTrial()
        score = sampler.objective(trial)

        assert isinstance(score, float)
        assert 0 <= score <= 1

    def test_optimization(self, sample_data):
        """Test full optimization runs."""
        X_train, y_train, _, _ = sample_data

        sampler = OptunaSampler(X_train, y_train, cv_folds=3, random_state=42)
        sampler.optimize(n_trials=2)

        assert sampler.study is not None
        assert sampler.best_trial is not None
        assert sampler.best_trial.value > 0

    def test_get_best_hyperparams(self, sample_data):
        """Test getting best hyperparameters."""
        X_train, y_train, _, _ = sample_data

        sampler = OptunaSampler(X_train, y_train, cv_folds=3, random_state=42)
        sampler.optimize(n_trials=2)

        hyperparams = sampler.get_best_hyperparams()

        assert "n_estimators" in hyperparams
        assert "max_depth" in hyperparams
        assert "max_features" in hyperparams
        assert 50 <= hyperparams["n_estimators"] <= 500
        assert 5 <= hyperparams["max_depth"] <= 50


class TestModelTrainer:
    """Tests for ModelTrainer class."""

    def test_initialization(self):
        """Test ModelTrainer initialization."""
        trainer = ModelTrainer(random_state=42)
        assert trainer.random_state == 42

    def test_train_model(self, sample_data):
        """Test model training."""
        X_train, y_train, _, _ = sample_data

        trainer = ModelTrainer(random_state=42)
        hyperparams = {
            "n_estimators": 50,
            "max_depth": 10,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "max_features": "sqrt",
            "random_state": 42,
            "n_jobs": -1,
        }

        model = trainer.train(X_train, y_train, hyperparams)

        assert model is not None
        assert model.n_estimators == 50
        assert len(model.feature_importances_) == X_train.shape[1]

    def test_save_model(self, sample_data):
        """Test model saving."""
        X_train, y_train, _, _ = sample_data

        trainer = ModelTrainer(random_state=42)
        hyperparams = {
            "n_estimators": 50,
            "max_depth": 10,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "max_features": "sqrt",
            "random_state": 42,
            "n_jobs": -1,
        }
        model = trainer.train(X_train, y_train, hyperparams)

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = Path(tmpdir) / "model.joblib"
            trainer.save_model(model, model_path)

            assert model_path.exists()

            import joblib

            loaded_model = joblib.load(model_path)
            assert loaded_model.n_estimators == 50


class TestModelEvaluator:
    """Tests for ModelEvaluator class."""

    def test_initialization(self):
        """Test ModelEvaluator initialization."""
        evaluator = ModelEvaluator(cv_folds=5, random_state=42)
        assert evaluator.cv_folds == 5
        assert evaluator.random_state == 42

    def test_evaluate_model(self, sample_data):
        """Test model evaluation."""
        X_train, y_train, X_test, y_test = sample_data

        trainer = ModelTrainer(random_state=42)
        hyperparams = {
            "n_estimators": 50,
            "max_depth": 10,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "max_features": "sqrt",
            "random_state": 42,
            "n_jobs": -1,
        }
        model = trainer.train(X_train, y_train, hyperparams)

        evaluator = ModelEvaluator(cv_folds=3, random_state=42)
        results = evaluator.evaluate_model(model, X_train, y_train, X_test, y_test, "Test")

        assert results["Model"] == "Test"
        assert "F1_CV_Mean" in results
        assert "F1_Test" in results
        assert "Accuracy_Test" in results
        assert 0 <= results["F1_Test"] <= 1
        assert 0 <= results["Accuracy_Test"] <= 1

    def test_compare_models(self, sample_data):
        """Test model comparison."""
        X_train, y_train, X_test, y_test = sample_data

        trainer = ModelTrainer(random_state=42)
        hyperparams = {
            "n_estimators": 50,
            "max_depth": 10,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "max_features": "sqrt",
            "random_state": 42,
            "n_jobs": -1,
        }

        default_model = trainer.train(X_train, y_train, hyperparams)
        optimized_model = trainer.train(X_train, y_train, hyperparams)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "comparison.csv"

            evaluator = ModelEvaluator(cv_folds=3, random_state=42)
            comparison_df = evaluator.compare_models(
                default_model,
                optimized_model,
                hyperparams,
                X_train,
                y_train,
                X_test,
                y_test,
                output_path,
            )

            assert output_path.exists()
            assert len(comparison_df) == 2
            assert "Default" in comparison_df["Model"].values
            assert "Optimized" in comparison_df["Model"].values
            assert "F1_Test" in comparison_df.columns
            assert (comparison_df["F1_Test"] >= 0).all()
            assert (comparison_df["F1_Test"] <= 1).all()


class TestFeatureImportanceExporter:
    """Tests for FeatureImportanceExporter class."""

    def test_export(self, sample_data):
        """Test feature importance export."""
        X_train, y_train, _, _ = sample_data

        trainer = ModelTrainer(random_state=42)
        hyperparams = {
            "n_estimators": 50,
            "max_depth": 10,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "max_features": "sqrt",
            "random_state": 42,
            "n_jobs": -1,
        }
        model = trainer.train(X_train, y_train, hyperparams)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            feature_names = X_train.columns.tolist()
            FeatureImportanceExporter.export(model, feature_names, output_dir)

            # Check CSV
            csv_path = output_dir / "feature_importances.csv"
            assert csv_path.exists()

            csv_df = pd.read_csv(csv_path)
            assert "feature_name" in csv_df.columns
            assert "importance_score" in csv_df.columns
            assert len(csv_df) == len(feature_names)

            # Check PNG
            png_path = output_dir / "feature_importances.png"
            assert png_path.exists()
            assert png_path.stat().st_size > 0


class TestDataLoading:
    """Tests for data loading utility."""

    def test_load_data_from_csv(self):
        """Test CSV data loading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create sample CSV files
            train_data = {
                "B2_Q1": np.random.randn(50),
                "B3_Q1": np.random.randn(50),
                "NDVI_Q1": np.random.randn(50),
                "Landcover": np.random.choice([0, 1, 2], 50),
                "LC_Nr": range(50),
                "LC_Out": range(50),
            }
            test_data = {
                "B2_Q1": np.random.randn(25),
                "B3_Q1": np.random.randn(25),
                "NDVI_Q1": np.random.randn(25),
                "Landcover": np.random.choice([0, 1, 2], 25),
                "LC_Nr": range(25),
                "LC_Out": range(25),
            }

            train_path = Path(tmpdir) / "train.csv"
            test_path = Path(tmpdir) / "test.csv"

            pd.DataFrame(train_data).to_csv(train_path, index=False)
            pd.DataFrame(test_data).to_csv(test_path, index=False)

            # Load data
            X_train, y_train, X_test, y_test = load_data_from_csv(train_path, test_path)

            # Check shapes
            assert X_train.shape[0] == 50
            assert X_test.shape[0] == 25
            assert len(y_train) == 50
            assert len(y_test) == 25

            # Check that metadata columns are dropped
            assert "LC_Nr" not in X_train.columns
            assert "LC_Out" not in X_train.columns
            assert "Landcover" not in X_train.columns

            # Check that feature columns are present
            assert "B2_Q1" in X_train.columns
            assert "NDVI_Q1" in X_train.columns
