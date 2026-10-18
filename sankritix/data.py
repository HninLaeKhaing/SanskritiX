from pathlib import Path

import tensorflow as tf

from sankritix.config import IMAGE_SIZE
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def list_class_names(split_dir: Path) -> list[str]:
    if not split_dir.is_dir():
        raise FileNotFoundError(f"Dataset split directory not found: {split_dir}")

    class_names = sorted(
        path.name for path in split_dir.iterdir() if path.is_dir()
    )
    if len(class_names) < 2:
        raise ValueError(
            f"Expected at least two class directories in {split_dir}, "
            f"found {len(class_names)}."
        )

    for class_name in class_names:
        class_dir = split_dir / class_name
        if not any(
            path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
            for path in class_dir.iterdir()
        ):
            raise ValueError(f"No supported images found in {class_dir}")

    return class_names


def load_split(
    split_dir: Path,
    class_names: list[str],
    batch_size: int,
    shuffle: bool,
) -> tf.data.Dataset:
    observed_classes = list_class_names(split_dir)
    if observed_classes != class_names:
        raise ValueError(
            f"Classes in {split_dir} do not match training classes. "
            f"Expected {class_names}, found {observed_classes}."
        )

    dataset = tf.keras.utils.image_dataset_from_directory(
        split_dir,
        labels="inferred",
        label_mode="int",
        class_names=class_names,
        image_size=IMAGE_SIZE,
        batch_size=batch_size,
        shuffle=shuffle,
        seed=42,
    )
    return dataset.prefetch(tf.data.AUTOTUNE)
