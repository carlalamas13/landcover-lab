
# Project Plan: LandCover AI Lab

## 1. Objective

Develop a multiclass satellite image classification system and experimentally compare traditional Machine Learning, computer vision, and Deep Learning approaches.

The project aims to investigate the strengths and limitations of each approach, evaluate their performance, and produce a reproducible implementation.

## 2. Problem Definition

Given a satellite image, the system will predict its corresponding land cover category.

The task will initially be formulated as a supervised multiclass classification problem.

## 3. Dataset

EuroSAT RGB has been selected for the initial experiments.

### Source

- Official dataset: https://zenodo.org/records/7711810
- Source repository: https://github.com/phelber/EuroSAT
- Original publication: https://doi.org/10.1109/JSTARS.2019.2918242

### Dataset Characteristics

- Approximately 27,000 labelled and georeferenced image patches.
- Ten land cover categories.
- RGB images with three colour channels.
- Image resolution of 64 × 64 pixels.
- JPEG image format in the RGB archive.

### Scope

The initial experiments will use RGB images to establish a reproducible classification baseline and compare traditional Machine Learning, computer vision, and Deep Learning approaches.

The 13-band multispectral version is outside the initial scope and may be evaluated as a future extension.

### Data Management

The dataset will be downloaded from the official Zenodo record and stored locally under `data/raw/`.

Downloaded data will remain outside version control. The repository will document the dataset source, relevant licensing information, and the procedures required to obtain it.

The final train, validation, and test splitting strategy will be selected after inspecting the dataset structure and assessing potential data leakage.


## 4. Experimental Methodology

The project will follow a reproducible experimental workflow.

- Characterize and explore the dataset.
- Define training, validation, and test sets.
- Establish an initial performance baseline.
- Train and compare selected models.
- Tune hyperparameters using development data.
- Evaluate the final models on a reserved test set.
- Analyse classification errors and document limitations.

The final splitting strategy will be determined after inspecting the dataset. Potential information leakage between related or geographically similar images will be considered.

Random seeds will be fixed where applicable, and comparable evaluation conditions will be maintained across experiments.

## 5. Planned Models

### Traditional Machine Learning

- Establish a simple baseline model.
- Train classifiers using image-derived features.
- Compare selected algorithms based on the initial results.

### Classical Computer Vision

- Explore colour spaces and visual characteristics.
- Extract image features, such as colour histograms and Histogram of Oriented Gradients (HOG).
- Evaluate classifiers trained on the extracted features.

### Deep Learning

- Implement a convolutional neural network (CNN) using PyTorch.
- Monitor training and validation loss and performance metrics.
- Investigate overfitting and regularization techniques.

### Transfer Learning

- Adapt a pretrained neural network architecture.
- Compare its performance with the custom CNN.
- Analyse classification errors across categories.

## 6. Evaluation Strategy

The following metrics will be considered:

- Accuracy.
- Per-class precision, recall, and F1-score.
- Macro F1-score.
- Confusion matrix.
- Training time and computational cost, where relevant.

Conclusions will consider both overall performance and class-specific behaviour.

## 7. Development Practices

- Use notebooks for exploratory analysis and experimentation.
- Gradually move reusable functionality into the `src/` package.
- Introduce automated tests as reusable components are developed.
- Store relevant figures and experimental outputs in `reports/`.
- Maintain the configuration required to reproduce the environment.

## 8. Project Phases

1. Environment setup and dataset review.
2. Exploratory data analysis.
3. Traditional Machine Learning baselines.
4. Classical computer vision techniques.
5. CNN development and training.
6. Transfer learning.
7. Final comparison and conclusions.
8. Optional interactive application.

## 9. Open Decisions

- Confirm the dataset version and access method.
- Define the data splitting strategy.
- Select the primary evaluation metrics.
- Determine the available training resources.
- Assess whether an interactive application adds value.

## 10. Status

Initial plan. Decisions will be reviewed as the dataset is explored and experimental results become available.
