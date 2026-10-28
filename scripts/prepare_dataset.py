from collections import Counter
from hashlib import md5
from pathlib import Path, PurePosixPath
from shutil import copyfileobj
from urllib.request import Request, urlopen
from zipfile import ZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
ARCHIVE_PATH = RAW_DIR / "EuroSAT_RGB.zip"
DATASET_DIR = RAW_DIR / "EuroSAT_RGB"

DOWNLOAD_URL = (
    "https://zenodo.org/records/7711810/files/"
    "EuroSAT_RGB.zip?download=1"
)
EXPECTED_MD5 = "f46e308c4d50d4bf32fedad2d3d62f3b"
EXPECTED_TOTAL = 27_000
CHUNK_SIZE = 1024 * 1024

EXPECTED_COUNTS = {
    "AnnualCrop": 3_000,
    "Forest": 3_000,
    "HerbaceousVegetation": 3_000,
    "Highway": 2_500,
    "Industrial": 2_500,
    "Pasture": 2_000,
    "PermanentCrop": 2_500,
    "Residential": 3_000,
    "River": 2_500,
    "SeaLake": 3_000,
}


def download_archive() -> None:
    """Download the dataset archive if it is not already present."""
    if ARCHIVE_PATH.is_file():
        print("Dataset archive already exists. Skipping download.")
        return

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    temporary_path = ARCHIVE_PATH.with_suffix(".zip.part")

    request = Request(
        DOWNLOAD_URL,
        headers={"User-Agent": "LandCover-AI-Lab/1.0"},
    )

    print("Downloading EuroSAT RGB dataset...")

    try:
        with urlopen(request, timeout=60) as response:
            with temporary_path.open("wb") as output:
                copyfileobj(response, output, length=CHUNK_SIZE)

        temporary_path.replace(ARCHIVE_PATH)
        print("Download completed.")
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def calculate_md5(path: Path) -> str:
    """Calculate the MD5 checksum for non-security integrity verification."""
    digest = md5(usedforsecurity=False)

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(CHUNK_SIZE),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def validate_archive() -> list[str]:
    """Validate the checksum and expected archive structure."""
    if not ARCHIVE_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset archive not found: {ARCHIVE_PATH}"
        )

    print("Verifying dataset checksum...")
    actual_md5 = calculate_md5(ARCHIVE_PATH)

    if actual_md5.lower() != EXPECTED_MD5:
        raise ValueError(
            "Dataset checksum mismatch. "
            "Check the downloaded archive before continuing."
        )

    print("Checksum verified.")

    with ZipFile(ARCHIVE_PATH, "r") as archive:
        corrupted_file = archive.testzip()

        if corrupted_file is not None:
            raise ValueError(
                f"Corrupted archive member: {corrupted_file}"
            )

        entries = [
            entry.filename
            for entry in archive.infolist()
            if not entry.is_dir()
        ]

    if len(entries) != EXPECTED_TOTAL:
        raise ValueError(
            f"Expected {EXPECTED_TOTAL} files, found {len(entries)}."
        )

    class_counts: Counter[str] = Counter()

    for name in entries:
        path = PurePosixPath(name)

        if (
            path.is_absolute()
            or ".." in path.parts
            or "\\" in name
            or len(path.parts) != 3
            or path.parts[0] != "EuroSAT_RGB"
        ):
            raise ValueError(f"Unexpected archive path: {name}")

        class_name = path.parts[1]

        if class_name not in EXPECTED_COUNTS:
            raise ValueError(f"Unexpected class: {class_name}")

        if path.suffix.lower() != ".jpg":
            raise ValueError(f"Unexpected file type: {name}")

        class_counts[class_name] += 1

    if dict(class_counts) != EXPECTED_COUNTS:
        raise ValueError(
            f"Unexpected class distribution: {dict(class_counts)}"
        )

    print(f"Archive contains {len(entries):,} JPEG images.")
    print(f"Number of classes: {len(class_counts)}")

    return entries


def count_extracted_images() -> Counter[str]:
    """Count JPEG images in each extracted class directory."""
    counts: Counter[str] = Counter()

    for class_name in EXPECTED_COUNTS:
        class_dir = DATASET_DIR / class_name

        if not class_dir.is_dir():
            return Counter()

        counts[class_name] = sum(
            1
            for path in class_dir.iterdir()
            if path.is_file() and path.suffix.lower() == ".jpg"
        )

    return counts


def extract_dataset(entries: list[str]) -> None:
    """Extract validated archive entries into the raw data directory."""
    current_counts = count_extracted_images()

    if dict(current_counts) == EXPECTED_COUNTS:
        print("Dataset is already extracted and validated.")
        return

    print("Extracting dataset images...")
    DATASET_DIR.mkdir(parents=True, exist_ok=True)

    with ZipFile(ARCHIVE_PATH, "r") as archive:
        for name in entries:
            destination = RAW_DIR.joinpath(
                *PurePosixPath(name).parts
            )
            destination.parent.mkdir(parents=True, exist_ok=True)

            with archive.open(name, "r") as source:
                with destination.open("wb") as output:
                    copyfileobj(source, output, length=CHUNK_SIZE)

    print("Extraction completed.")


def validate_extracted_dataset() -> None:
    """Verify the extracted images and class distribution."""
    counts = count_extracted_images()

    if dict(counts) != EXPECTED_COUNTS:
        raise ValueError(
            f"Extracted dataset validation failed: {dict(counts)}"
        )

    print("\nDataset preparation completed successfully.")
    print("\nImages per class:")

    for class_name in sorted(counts):
        print(f"{class_name}: {counts[class_name]:,}")

    print(f"\nTotal images: {sum(counts.values()):,}")
    print(f"Dataset location: {DATASET_DIR}")


def main() -> None:
    """Run the dataset preparation workflow."""
    download_archive()
    entries = validate_archive()
    extract_dataset(entries)
    validate_extracted_dataset()


if __name__ == "__main__":
    main()
