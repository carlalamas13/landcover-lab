
"""Create reproducible stratified train, validation, and test splits."""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = PROJECT_ROOT / "data" / "raw" / "EuroSAT_RGB"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "split_manifest.csv"

EXPECTED_CLASSES = [
    "AnnualCrop",
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Pasture",
    "PermanentCrop",
    "Residential",
    "River",
    "SeaLake",
]

EXPECTED_TOTAL_IMAGES = 27_000
RANDOM_STATE = 42


def build_dataset_index() -> pd.DataFrame:
    """Create an index of image paths and their class labels."""
    if not DATASET_DIR.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {DATASET_DIR}. "
            "Run scripts/prepare_dataset.py first."
        )

    class_dirs = sorted(
        path for path in DATASET_DIR.iterdir()
        if path.is_dir()
    )
    actual_classes = sorted(path.name for path in class_dirs)

    if actual_classes != sorted(EXPECTED_CLASSES):
        raise ValueError(
            f"Unexpected class directories: {actual_classes}"
        )

    records = []

    for class_dir in class_dirs:
        image_paths = sorted(
            path for path in class_dir.iterdir()
            if path.is_file() and path.suffix.lower() == ".jpg"
        )

        for image_path in image_paths:
            records.append(
                {
                    "filepath": image_path.relative_to(
                        PROJECT_ROOT
                    ).as_posix(),
                    "label": class_dir.name,
                }
            )

    samples = pd.DataFrame(records)

    if len(samples) != EXPECTED_TOTAL_IMAGES:
        raise ValueError(
            f"Expected {EXPECTED_TOTAL_IMAGES} images, "
            f"found {len(samples)}."
        )

    if samples["filepath"].duplicated().any():
        raise ValueError("Duplicate image paths were found.")

    return samples


def create_splits(samples: pd.DataFrame) -> pd.DataFrame:
    """Create a reproducible 70/15/15 stratified split."""
    train_samples, temporary_samples = train_test_split(
        samples,
        test_size=0.30,
        stratify=samples["label"],
        random_state=RANDOM_STATE,
    )

    validation_samples, test_samples = train_test_split(
        temporary_samples,
        test_size=0.50,
        stratify=temporary_samples["label"],
        random_state=RANDOM_STATE,
    )

    manifest = pd.concat(
        [
            train_samples.assign(split="train"),
            validation_samples.assign(split="validation"),
            test_samples.assign(split="test"),
        ],
        ignore_index=True,
    )

    return manifest[["filepath", "label", "split"]]


def validate_splits(manifest: pd.DataFrame) -> None:
    """Validate split sizes, labels, and class coverage."""
    expected_sizes = {
        "train": 18_900,
        "validation": 4_050,
        "test": 4_050,
    }

    actual_sizes = (
        manifest["split"].value_counts().to_dict()
    )

    if actual_sizes != expected_sizes:
        raise ValueError(
            f"Unexpected split sizes: {actual_sizes}"
        )

    if manifest["filepath"].duplicated().any():
        raise ValueError(
            "An image appears more than once in the manifest."
        )

    if set(manifest["label"]) != set(EXPECTED_CLASSES):
        raise ValueError(
            "The split manifest does not contain all expected classes."
        )

    class_counts = pd.crosstab(
        manifest["label"],
        manifest["split"],
    ).reindex(
        index=EXPECTED_CLASSES,
        columns=["train", "validation", "test"],
        fill_value=0,
    )

    if (class_counts == 0).any().any():
        raise ValueError(
            "At least one class is missing from a split."
        )


def main() -> None:
    """Build, validate, and save the split manifest."""
    samples = build_dataset_index()
    manifest = create_splits(samples)

    validate_splits(manifest)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    manifest.to_csv(OUTPUT_PATH, index=False)

    print("Dataset split completed successfully.")
    print(f"Total images: {len(manifest):,}")
    print("\nImages per split:")
    print(
        manifest["split"]
        .value_counts()
        .reindex(["train", "validation", "test"])
        .to_string()
    )

    print("\nClass distribution by split:")
    print(
        pd.crosstab(
            manifest["label"],
            manifest["split"],
        )
        .reindex(
            index=EXPECTED_CLASSES,
            columns=["train", "validation", "test"],
        )
        .to_string()
    )

    print(f"\nSplit manifest saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
