import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf

from sankritix.data import list_class_names, load_split
from sankritix.model import build_model
from sankritix.predict import derive_decision_guidance


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train and evaluate the SanskritiX image classifier."
    )
    parser.add_argument("--data-dir", type=Path, default=Path("data/images"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=32)
    return parser.parse_args()


def collect_predictions(
    model: tf.keras.Model, dataset: tf.data.Dataset
) -> tuple[np.ndarray, np.ndarray]:
    labels = np.concatenate([batch_labels.numpy() for _, batch_labels in dataset])
    scores = model.predict(dataset, verbose=0)
    return labels, scores


def main() -> None:
    args = parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        raise ValueError("--epochs and --batch-size must be positive integers.")

    train_dir = args.data_dir / "train"
    class_names = list_class_names(train_dir)
    train_data = load_split(train_dir, class_names, args.batch_size, shuffle=True)
    val_data = load_split(
        args.data_dir / "val", class_names, args.batch_size, shuffle=False
    )
    test_data = load_split(
        args.data_dir / "test", class_names, args.batch_size, shuffle=False
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    model_path = args.output_dir / "sankritix.keras"
    model = build_model(len(class_names))
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            model_path,
            monitor="val_loss",
            save_best_only=True,
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
        ),
    ]
    model.fit(
        train_data,
        validation_data=val_data,
        epochs=args.epochs,
        callbacks=callbacks,
    )

    best_model = tf.keras.models.load_model(model_path)
    val_labels, val_scores = collect_predictions(best_model, val_data)
    labels, test_scores = collect_predictions(best_model, test_data)
    predictions = test_scores.argmax(axis=1)
    report = classification_report(
        labels,
        predictions,
        labels=range(len(class_names)),
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(labels, predictions, labels=range(len(class_names)))

    (args.output_dir / "class_names.json").write_text(
        json.dumps(class_names, indent=2) + "\n", encoding="utf-8"
    )
    guidance = derive_decision_guidance(val_labels, val_scores)
    (args.output_dir / "decision_guidance.json").write_text(
        json.dumps(guidance, indent=2) + "\n", encoding="utf-8"
    )
    (args.output_dir / "test_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    np.savetxt(
        args.output_dir / "confusion_matrix.csv",
        matrix,
        delimiter=",",
        fmt="%d",
        header="rows=true labels; columns=predicted labels in class_names.json",
        comments="",
    )
    print(f"Saved model and test metrics to {args.output_dir}")
    print(
        classification_report(
            labels,
            predictions,
            target_names=class_names,
            zero_division=0,
        )
    )


if __name__ == "__main__":
    main()
