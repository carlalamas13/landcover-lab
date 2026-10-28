# LandCover AI Lab

## Overview

LandCover AI Lab is a Machine learning and Deep Learning project focused on satellite image classification.

The goal is to investigate and compare traditional Machine Learning algorithms, computer vision techniques, and Deep Learning architectures for multiclass land cover classification.

The project follows an experimental approach, from dataset exploration and baseline modelling to convolutional neural networks and transfer learning.

## Objectives

- Explore and characterize a labelled satellite imagery dataset.
- Establish baseline models using traditional Machine Learning algorithms.
- Investigate feature extraction techniques for computer vision.
- Implement and train convolutional neural networks using PyTorch.
- Evaluate transfer learning with a pretrained architecture.
- Compare model performance using appropriate evaluation metrics.
- Analyse classification errors and document experimental findings.

## Planned Technologies

- Python
- NumPy and Pandas
- Matplotlib and Seaborn
- Scikit-learn
- OpenCV
- PyTorch
- Git

## Project Workflow

1. Dataset exploration and preparation.
2. Traditional Machine Learning baselines.
3. Classical computer vision techniques.
4. Convolutional neural network development.
5. Transfer learning and model comparison.
6. Final evaluation and optional interactive application.

## Dataset

EuroSAT is the selected dataset for the initial experiments.

It contains approximately 27,000 labelled and georeferenced Sentinel-2 image patches across ten land cover classes.

The project will initially use the RGB version, consisting of 64 × 64 pixel images with three colour channels. The multispectral version, which includes all 13 Sentinel-2 bands, may be investigated as a future extension.

### Data Sources

- [Official EuroSAT dataset (Zenodo)](https://zenodo.org/records/7711810)
- [EuroSAT source repository](https://github.com/phelber/EuroSAT)
- [Original research paper](https://doi.org/10.1109/JSTARS.2019.2918242)

### Data Management and Licensing

The EuroSAT repository identifies the dataset licence as MIT. The applicable Copernicus Sentinel data terms should also be reviewed.

Downloaded datasets and trained model weights will remain outside version control. Only the code, documentation, and relevant experimental results will be stored in this repository.

## Getting Started

### 1. Set Up the Environment

Create and activate a Python virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Prepare the Dataset

Run the dataset preparation script from the project root:

```powershell
python scripts/prepare_dataset.py
```

The script automatically:

- Downloads the EuroSAT RGB archive if it is not available locally.
- Verifies the archive checksum.
- Validates the expected directory structure and class distribution.
- Extracts the images into `data/raw/EuroSAT_RGB/`.
- Checks the extracted image counts.

The dataset is stored locally and is excluded from version control.

### 3. Explore the Data

Once the dataset has been prepared, run the exploratory analysis notebook in the `notebooks/` directory using Jupyter or Visual Studio Code.

## Project Status

In development. Experimental results will be added as the implementation progresses.
