#!/usr/bin/env python3
"""Script to prepare land cover train/test data using the data_preparation module."""

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_preparation import LandCoverDataSplitter, SpectralIndexComputer


def main():
    """Main function to run data preparation."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    # Define paths
    data_dir = Path(__file__).parent.parent / "data"
    raw_data_path = data_dir / "raw_data.csv"
    train_output_path = data_dir / "train.csv"
    test_output_path = data_dir / "test.csv"

    # Check if input exists
    if not raw_data_path.exists():
        logger.error(f"Raw data file not found at {raw_data_path}")
        sys.exit(1)

    logger.info("Starting data preparation...")

    # Initialize splitter
    splitter = LandCoverDataSplitter(raw_data_path, random_state=42)

    # Process data
    splitter.load_data()
    logger.info(f"Loaded {splitter.df.height} rows from {raw_data_path}")

    splitter.filter_classes(exclude=["Deforestation"])
    logger.info(f"After filtering: {splitter.df.height} rows")

    splitter.normalize_labels()
    logger.info("Normalized labels")

    # Define class-specific sampling
    class_samples = {
        "Forest": 500,
        "Cropland": 500,
        "Wetland": 500,
        "Shrub": 500,
        "Grass": 500,
        "Bare": None,
        "Water": None,
        "Built Up": None,
    }

    # Perform balanced split
    train_df, test_df = splitter.balanced_split(class_samples, train_fraction=0.7)

    logger.info(f"Train set: {train_df.height} rows")
    logger.info(f"Test set: {test_df.height} rows")

    # Add spectral indices
    logger.info("Computing spectral indices...")
    train_computer = SpectralIndexComputer(train_df)
    train_df = train_computer.compute_all_indices()

    test_computer = SpectralIndexComputer(test_df)
    test_df = test_computer.compute_all_indices()

    logger.info(f"Train set after indices: {train_df.shape[1]} columns")
    logger.info(f"Test set after indices: {test_df.shape[1]} columns")

    # Save outputs
    train_df.write_csv(train_output_path)
    test_df.write_csv(test_output_path)

    logger.info(f"Saved train data to {train_output_path}")
    logger.info(f"Saved test data to {test_output_path}")

    logger.info("Data preparation completed successfully!")


if __name__ == "__main__":
    main()
