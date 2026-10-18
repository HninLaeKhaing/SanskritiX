# SanskritiX

SanskritiX is a computer-vision learning project for exploring Indian art traditions. It combines an image-classification baseline with introductory learning cards and a short knowledge check.

The supplied dataset covers eight painting traditions: Gond, Kalighat, Kangra, Kerala, Madhubani, Mandana, Pichwai, and Warli. A prediction is a visual suggestion, not proof of an artwork's origin or authenticity.

## Requirements

- Python 3.10–3.12
- TensorFlow, scikit-learn, and the packages in `requirements.txt`
- A labeled image dataset arranged as described in [`data/README.md`](data/README.md)

Create and activate a virtual environment, then install dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Dataset layout

The supplied ZIP dataset can be prepared into class subfolders under `data/images`:

```powershell
python -m sankritix.prepare_dataset
```

This creates a deterministic 70/15/15 split for its eight available labels. See [`data/README.md`](data/README.md) for provenance and image reuse cautions. If you prepare a different dataset, use the same split folder layout:

```text
data/images/
  train/
    gond/
    kalighat/
    kangra/
    kerala/
    madhubani/
    mandana/
    pichwai/
    warli/
  val/
    ...same class folders...
  test/
    ...same class folders...
```

See [`data/README.md`](data/README.md) before collecting images. Keep a record of each image's source and license, avoid duplicate or near-duplicate images across splits, and do not use test images for training decisions.

## Train and evaluate

From the project root:

```powershell
python -m sankritix.train --data-dir data/images --output-dir artifacts
```

The trainer uses an ImageNet-pretrained MobileNetV2 as a frozen feature extractor, selects the best classifier checkpoint using validation loss, and evaluates it once on the held-out test split. The first run may download pretrained weights. Model files and reports are written to `artifacts/` (ignored by Git).

## Classify an image

```powershell
python -m sankritix.predict path\to\image.jpg --artifacts-dir artifacts
```

Predictions below the default 0.55 confidence threshold are explicitly marked uncertain. Adjust the threshold with `--threshold` only after considering validation results; a softmax score is not a calibrated probability.

## Run the web demo

```powershell
streamlit run sankritix/app.py
```

The app includes an artwork-identification tab, an explorer with history, region, materials, visual features, reflection prompts, and further-reading links for all eight labels, plus a three-question sequential quiz for each tradition. Each response shows immediate feedback and an explanation before the learner advances; session progress is displayed and each quiz can be replayed. After an image is classified, results include a learning guide, comparison with the runner-up label, an optional Grad-CAM attention overlay, and source links. Grad-CAM shows model attention, not cultural evidence. Validation-derived confidence and top-label-margin heuristics flag tentative predictions; they are not calibrated probabilities. Users can save result summaries for the browser session and download them as JSON; uploaded images are not saved. Quiz progress is also session-only. An expandable transparency panel describes the dataset and license caveats. The learning cards remain available if the model has not been trained. Before training, photo upload is disabled and the sample result card is clearly marked as illustrative. The model does not establish provenance or authenticity.

## Public deployment

The public deployment includes the trained model, class labels, and validation-based decision guidance so that image uploads, classification, and Grad-CAM attention maps work. It does not include the source artwork archive or extracted training images. Image-level reuse rights for the source dataset were not verified; the model weights are published with that limitation disclosed. Confirm dataset and model redistribution terms before reusing or redistributing them.

The app is hosted on [Streamlit Community Cloud](https://sanskritix.streamlit.app/) from this repository's `main` branch, using `sankritix/app.py` and Python 3.12. Dependencies are installed from `requirements.txt`.

## Run tests

```powershell
pip install -r requirements-dev.txt
python -m pytest
```

## Current scope and limitations

- The model only recognizes the eight labels in the supplied dataset; it cannot identify every Indian art form.
- Photographs, backgrounds, framing, and image quality can affect predictions.
- The observed held-out test accuracy is about 79% on 149 images from a random image-level split. Possible near-duplicates or shared sources across splits may inflate this estimate; it is not a guarantee of real-world accuracy.
- A high confidence score does not establish provenance, authenticity, or cultural meaning.
- The archive's MIT notice does not verify the reuse rights of each artwork image. Confirm image-level terms before publishing or redistributing.
- Learning cards are short introductions, not definitive histories. Some references are overview or collection-search pages; check the cited material and consult artists, community knowledge holders, museums, and scholarly sources before using the material as authoritative teaching content.

## Project layout

```text
sankritix/          training and prediction code
                    Streamlit image-exploration demo
tests/              focused unit tests
data/               dataset instructions (images are not committed)
artifacts/          generated model and evaluation outputs (not committed)
```
