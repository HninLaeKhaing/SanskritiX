from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image, UnidentifiedImageError

from sankritix.config import IMAGE_SIZE

if TYPE_CHECKING:
    import tensorflow as tf


def predict_image(model: tf.keras.Model, image: Image.Image) -> np.ndarray:
    resized = image.convert("RGB").resize(IMAGE_SIZE)
    pixels = np.asarray(resized, dtype=np.float32)
    return model.predict(np.expand_dims(pixels, axis=0), verbose=0)[0]


def rank_predictions(
    scores: np.ndarray,
    class_names: list[str],
    top_k: int = 3,
) -> list[tuple[str, float]]:
    if scores.ndim != 1 or len(scores) != len(class_names):
        raise ValueError("Prediction scores must match the class names.")
    if not np.isfinite(scores).all():
        raise ValueError("Prediction scores must all be finite.")
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    ranked_indices = np.argsort(scores)[::-1][: min(top_k, len(class_names))]
    return [(class_names[int(index)], float(scores[index])) for index in ranked_indices]


def derive_decision_guidance(
    labels: np.ndarray,
    scores: np.ndarray,
    correct_percentile: float = 10.0,
) -> dict[str, float | int | str]:
    if scores.ndim != 2 or len(labels) != len(scores) or scores.shape[1] < 2:
        raise ValueError("Validation labels and class scores have incompatible shapes.")
    if not np.isfinite(scores).all():
        raise ValueError("Validation scores must all be finite.")
    if not 0.0 <= correct_percentile <= 100.0:
        raise ValueError("correct_percentile must be between 0 and 100.")

    order = np.argsort(scores, axis=1)
    best_indices = order[:, -1]
    confidence = scores[np.arange(len(scores)), best_indices]
    margin = confidence - scores[np.arange(len(scores)), order[:, -2]]
    correct = best_indices == labels
    if not correct.any():
        return {
            "confidence_threshold": 1.0,
            "margin_threshold": 1.0,
            "correct_validation_samples": 0,
            "correct_percentile": correct_percentile,
            "method": "validation_correct_prediction_lower_percentile",
        }

    return {
        "confidence_threshold": float(
            np.percentile(confidence[correct], correct_percentile)
        ),
        "margin_threshold": float(np.percentile(margin[correct], correct_percentile)),
        "correct_validation_samples": int(correct.sum()),
        "correct_percentile": correct_percentile,
        "method": "validation_correct_prediction_lower_percentile",
    }


def assess_prediction(
    ranked: list[tuple[str, float]],
    guidance: dict[str, float | int | str],
) -> tuple[bool, str]:
    if not ranked:
        raise ValueError("At least one ranked prediction is required.")
    confidence_threshold = float(guidance["confidence_threshold"])
    margin_threshold = float(guidance["margin_threshold"])
    confidence = ranked[0][1]
    margin = confidence - ranked[1][1] if len(ranked) > 1 else confidence

    if confidence < confidence_threshold:
        return True, "The leading score is below the validation-based guide."
    if margin < margin_threshold:
        return True, "The two leading labels are close under the validation-based guide."
    return False, "The leading match is clearer under the validation-based guide."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify an image using a trained SanskritiX model."
    )
    parser.add_argument("image", type=Path)
    parser.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument("--top-k", type=int, default=3)
    return parser.parse_args()


def load_image(image_path: Path) -> np.ndarray:
    try:
        with Image.open(image_path) as image:
            return np.asarray(image.convert("RGB").resize(IMAGE_SIZE), dtype=np.float32)
    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found: {image_path}") from None
    except (UnidentifiedImageError, OSError) as error:
        raise ValueError(f"Could not read image '{image_path}': {error}") from error


def main() -> None:
    args = parse_args()
    if not 0.0 <= args.threshold <= 1.0:
        raise ValueError("--threshold must be between 0 and 1.")
    if args.top_k < 1:
        raise ValueError("--top-k must be at least 1.")

    model_path = args.artifacts_dir / "sankritix.keras"
    names_path = args.artifacts_dir / "class_names.json"
    if not model_path.is_file() or not names_path.is_file():
        raise FileNotFoundError(
            f"Model artifacts not found in {args.artifacts_dir}. "
            "Train the model first."
        )

    class_names = json.loads(names_path.read_text(encoding="utf-8"))
    import tensorflow as tf

    model = tf.keras.models.load_model(model_path)
    with Image.open(args.image) as image:
        predictions = rank_predictions(
            predict_image(model, image),
            class_names,
            top_k=args.top_k,
        )
    best_class, confidence = predictions[0]

    print(f"Prediction: {best_class}")
    print(f"Score: {confidence:.1%}")
    if confidence < args.threshold:
        print("Result: uncertain (below the selected confidence threshold)")
    print("Other matches:")
    for class_name, score in predictions:
        print(f"  {class_name}: {score:.1%}")
    print("Visual classification is not proof of origin or authenticity.")


if __name__ == "__main__":
    main()
