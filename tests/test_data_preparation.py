"""Unit tests for data_preparation module."""

import tempfile
from pathlib import Path

import polars as pl
import pytest

from src.data_preparation import LandCoverDataSplitter, SpectralIndexComputer


@pytest.fixture
def sample_data():
    """Create sample land cover data for testing."""
    data = {
        "B2_Q1": [100, 200, 150, 180, 120, 190],
        "B3_Q1": [200, 300, 250, 280, 220, 290],
        "B4_Q1": [150, 250, 200, 230, 170, 240],
        "B8_Q1": [300, 400, 350, 380, 320, 390],
        "B12_Q1": [100, 150, 120, 140, 110, 130],
        "LC_Nr": [1, 2, 3, 1, 2, 3],
        "LC_Out": ["forest", "cropland", "wetland", "forest", "cropland", "wetland"],
        "Landcover": ["Forest", "Cropland", "Wetland", "Forest", "Cropland", "Wetland"],
    }
    return pl.DataFrame(data)


@pytest.fixture
def temp_csv(sample_data):
    """Create a temporary CSV file with sample data."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        sample_data.write_csv(f.name)
        return f.name


class TestLandCoverDataSplitter:
    """Test cases for LandCoverDataSplitter class."""

    def test_init(self, temp_csv):
        """Test initialization."""
        splitter = LandCoverDataSplitter(temp_csv)
        assert splitter.data_path == Path(temp_csv)
        assert splitter.random_state == 42
        assert splitter.df is None

    def test_load_data(self, temp_csv, sample_data):
        """Test data loading."""
        splitter = LandCoverDataSplitter(temp_csv)
        result = splitter.load_data()
        assert isinstance(result, LandCoverDataSplitter)
        assert splitter.df.height == sample_data.height

    def test_filter_classes(self, temp_csv):
        """Test class filtering."""
        splitter = LandCoverDataSplitter(temp_csv)
        splitter.load_data()
        splitter.df = splitter.df.with_columns(
            pl.when(pl.col("Landcover") == "Forest")
            .then(pl.lit("Deforestation"))
            .otherwise(pl.col("Landcover"))
            .alias("Landcover")
        )
        splitter.filter_classes(["Deforestation"])
        assert "Deforestation" not in splitter.df["Landcover"].to_list()

    def test_normalize_labels(self, temp_csv):
        """Test label normalization."""
        splitter = LandCoverDataSplitter(temp_csv)
        splitter.load_data()
        splitter.df = splitter.df.with_columns(
            pl.col("Landcover").str.to_lowercase().alias("Landcover")
        )
        splitter.normalize_labels()
        labels = splitter.df["Landcover"].unique().to_list()
        assert all(label.istitle() for label in labels)

    def test_balanced_split(self, temp_csv):
        """Test balanced train/test splitting."""
        splitter = LandCoverDataSplitter(temp_csv, random_state=42)
        splitter.load_data()
        splitter.normalize_labels()
        class_samples = {"Forest": 1, "Cropland": 1, "Wetland": 1}
        train_df, test_df = splitter.balanced_split(class_samples, train_fraction=0.5)
        assert train_df.height + test_df.height == splitter.df.height
        assert train_df.filter(pl.col("Landcover") == "Forest").height == 1

    def test_balanced_split_no_downsampling(self, temp_csv):
        """Test split without downsampling."""
        splitter = LandCoverDataSplitter(temp_csv, random_state=42)
        splitter.load_data()
        class_samples = {"Forest": None, "Cropland": None, "Wetland": None}
        train_df, test_df = splitter.balanced_split(class_samples, train_fraction=0.6)
        assert train_df.height + test_df.height == splitter.df.height

    def test_load_data_without_file(self):
        """Test error when file doesn't exist."""
        splitter = LandCoverDataSplitter("nonexistent.csv")
        with pytest.raises(FileNotFoundError):
            splitter.load_data()


class TestSpectralIndexComputer:
    """Test cases for SpectralIndexComputer class."""

    def test_add_ndvi(self, sample_data):
        """Test NDVI computation."""
        computer = SpectralIndexComputer(sample_data)
        result = computer.add_ndvi("B8_Q1", "B4_Q1", "NDVI")
        assert "NDVI" in result.df.columns
        expected = (300 - 150) / (300 + 150)
        assert abs(result.df["NDVI"][0] - expected) < 1e-6

    def test_compute_all_indices(self, sample_data):
        """Test computing all indices."""
        computer = SpectralIndexComputer(sample_data)
        result = computer.compute_all_indices(quarters=[1])
        expected_cols = ["NDVI_Q1", "NDWI_MCF_Q1", "NDWI_GAO_Q1", "SAVI_Q1", "EVI_Q1"]
        for col in expected_cols:
            assert col in result.columns

    def test_compute_all_indices_missing_bands(self, sample_data):
        """Test with missing bands."""
        df_missing = sample_data.drop(["B12_Q1"])
        computer = SpectralIndexComputer(df_missing)
        result = computer.compute_all_indices(quarters=[1])
        assert "NDWI_GAO_Q1" not in result.columns
        assert "NDVI_Q1" in result.columns
