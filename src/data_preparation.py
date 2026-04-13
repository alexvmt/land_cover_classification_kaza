"""Data preparation module for land cover classification.

This module provides classes for loading, processing, and splitting land cover data
into balanced train/test sets using Polars for efficient data handling.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import polars as pl


class LandCoverDataSplitter:
    """Handles loading, filtering, normalizing, and balanced splitting of land cover data."""

    def __init__(self, data_path: str | Path, random_state: int = 42):
        """Initialize the data splitter.

        Args:
            data_path: Path to the raw CSV data file.
            random_state: Random seed for reproducible shuffling.
        """
        self.data_path = Path(data_path)
        self.random_state = random_state
        self.df: Optional[pl.DataFrame] = None

    def load_data(self) -> "LandCoverDataSplitter":
        """Load the raw data from CSV.

        Drops remote sensing metadata columns if present.

        Returns:
            Self for method chaining.
        """
        self.df = pl.read_csv(self.data_path)

        # Drop metadata columns if they exist
        columns_to_drop = []
        if "system:index" in self.df.columns:
            columns_to_drop.append("system:index")
        if ".geo" in self.df.columns:
            columns_to_drop.append(".geo")

        if columns_to_drop:
            self.df = self.df.drop(columns_to_drop)

        return self

    def filter_classes(self, exclude: Optional[List[str]] = None) -> "LandCoverDataSplitter":
        """Filter out unwanted land cover classes.

        Args:
            exclude: List of class names to exclude. Defaults to ["Deforestation"].

        Returns:
            Self for method chaining.
        """
        if exclude is None:
            exclude = ["Deforestation"]
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        self.df = self.df.filter(~pl.col("Landcover").is_in(exclude))
        return self

    def normalize_labels(self) -> "LandCoverDataSplitter":
        """Normalize land cover labels by capitalizing them.

        Returns:
            Self for method chaining.
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        self.df = self.df.with_columns(pl.col("Landcover").str.to_titlecase().alias("Landcover"))
        return self

    def balanced_split(
        self, class_samples: Dict[str, Optional[int]], train_fraction: float = 0.7
    ) -> Tuple[pl.DataFrame, pl.DataFrame]:
        """Perform balanced train/test split with per-class downsampling.

        Args:
            class_samples: Dict mapping class names to desired train samples.
                          Use None for a class to include all available samples.
            train_fraction: Fraction of data to use for training (default 0.7).

        Returns:
            Tuple of (train_df, test_df).
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        train_dfs = []
        test_dfs = []

        unique_classes = self.df.select("Landcover").unique().to_series().to_list()

        for class_name in unique_classes:
            df_class = self.df.filter(pl.col("Landcover") == class_name)

            # Shuffle the data
            df_class = df_class.sample(fraction=1.0, seed=self.random_state, shuffle=True)

            # Calculate split indices
            n_total = df_class.height
            n_train = int(n_total * train_fraction)
            n_test = n_total - n_train

            # Split
            train_class = df_class.head(n_train)
            test_class = df_class.tail(n_test)

            # Downsample train if specified
            desired = class_samples.get(class_name)
            if desired is not None and desired < n_train:
                train_class = train_class.head(desired)

            train_dfs.append(train_class)
            test_dfs.append(test_class)

        # Concatenate all classes
        train_df = pl.concat(train_dfs)
        test_df = pl.concat(test_dfs)

        # Shuffle final datasets
        train_df = train_df.sample(fraction=1.0, seed=self.random_state, shuffle=True)
        test_df = test_df.sample(fraction=1.0, seed=self.random_state, shuffle=True)

        return train_df, test_df


class SpectralIndexComputer:
    """Computes spectral vegetation and water indices for remote sensing data.

    Supports NDVI, NDWI variants, SAVI, and EVI for quarterly data.
    """

    def __init__(self, df: pl.DataFrame):
        """Initialize with a dataframe containing spectral bands.

        Args:
            df: Polars DataFrame with spectral columns.
        """
        self.df = df

    def add_ndvi(self, nir_col: str, red_col: str, output_col: str) -> "SpectralIndexComputer":
        """Add Normalized Difference Vegetation Index.

        NDVI = (NIR - RED) / (NIR + RED)

        Args:
            nir_col: NIR band column name.
            red_col: Red band column name.
            output_col: Output column name.

        Returns:
            Self for method chaining.
        """
        self.df = self.df.with_columns(
            ((pl.col(nir_col) - pl.col(red_col)) / (pl.col(nir_col) + pl.col(red_col))).alias(
                output_col
            )
        )
        return self

    def add_ndwi_mcf(
        self, green_col: str, nir_col: str, output_col: str
    ) -> "SpectralIndexComputer":
        """Add Normalized Difference Water Index (McFeeters).

        NDWI = (GREEN - NIR) / (GREEN + NIR)

        Args:
            green_col: Green band column name.
            nir_col: NIR band column name.
            output_col: Output column name.

        Returns:
            Self for method chaining.
        """
        self.df = self.df.with_columns(
            ((pl.col(green_col) - pl.col(nir_col)) / (pl.col(green_col) + pl.col(nir_col))).alias(
                output_col
            )
        )
        return self

    def add_ndwi_gao(self, nir_col: str, swir_col: str, output_col: str) -> "SpectralIndexComputer":
        """Add Normalized Difference Water Index (Gao).

        NDWI = (NIR - SWIR) / (NIR + SWIR)

        Args:
            nir_col: NIR band column name.
            swir_col: SWIR band column name.
            output_col: Output column name.

        Returns:
            Self for method chaining.
        """
        self.df = self.df.with_columns(
            ((pl.col(nir_col) - pl.col(swir_col)) / (pl.col(nir_col) + pl.col(swir_col))).alias(
                output_col
            )
        )
        return self

    def add_savi(
        self, nir_col: str, red_col: str, output_col: str, L: float = 0.5
    ) -> "SpectralIndexComputer":
        """Add Soil Adjusted Vegetation Index.

        SAVI = [(NIR - RED) / (NIR + RED + L)] * (1 + L)

        Args:
            nir_col: NIR band column name.
            red_col: Red band column name.
            output_col: Output column name.
            L: Soil adjustment factor (default 0.5).

        Returns:
            Self for method chaining.
        """
        self.df = self.df.with_columns(
            (
                ((pl.col(nir_col) - pl.col(red_col)) / (pl.col(nir_col) + pl.col(red_col) + L))
                * (1 + L)
            ).alias(output_col)
        )
        return self

    def add_evi(
        self, nir_col: str, red_col: str, blue_col: str, output_col: str
    ) -> "SpectralIndexComputer":
        """Add Enhanced Vegetation Index.

        EVI = 2.5 * [(NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)]

        Args:
            nir_col: NIR band column name.
            red_col: Red band column name.
            blue_col: Blue band column name.
            output_col: Output column name.

        Returns:
            Self for method chaining.
        """
        self.df = self.df.with_columns(
            (
                2.5
                * (pl.col(nir_col) - pl.col(red_col))
                / (pl.col(nir_col) + 6 * pl.col(red_col) - 7.5 * pl.col(blue_col) + 1)
            ).alias(output_col)
        )
        return self

    def compute_all_indices(self, quarters: Optional[List[int]] = None) -> pl.DataFrame:
        """Compute all indices for all specified quarters.

        Only computes indices for which all required bands are present.

        Args:
            quarters: List of quarters to compute indices for. Defaults to [1, 2, 3, 4].

        Returns:
            DataFrame with added index columns.
        """
        if quarters is None:
            quarters = [1, 2, 3, 4]
        for q in quarters:
            # Band mappings for quarter q
            bands = {
                "blue": f"B2_Q{q}",
                "green": f"B3_Q{q}",
                "red": f"B4_Q{q}",
                "nir": f"B8_Q{q}",
                "swir": f"B12_Q{q}",
            }

            # Compute each index if bands are available
            if bands["nir"] in self.df.columns and bands["red"] in self.df.columns:
                self.add_ndvi(bands["nir"], bands["red"], f"NDVI_Q{q}")

            if bands["green"] in self.df.columns and bands["nir"] in self.df.columns:
                self.add_ndwi_mcf(bands["green"], bands["nir"], f"NDWI_MCF_Q{q}")

            if bands["nir"] in self.df.columns and bands["swir"] in self.df.columns:
                self.add_ndwi_gao(bands["nir"], bands["swir"], f"NDWI_GAO_Q{q}")

            if bands["nir"] in self.df.columns and bands["red"] in self.df.columns:
                self.add_savi(bands["nir"], bands["red"], f"SAVI_Q{q}")

            if (
                bands["nir"] in self.df.columns
                and bands["red"] in self.df.columns
                and bands["blue"] in self.df.columns
            ):
                self.add_evi(bands["nir"], bands["red"], bands["blue"], f"EVI_Q{q}")

        return self.df
