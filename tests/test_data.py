from pathlib import Path

import pytest
from PIL import Image

from sankritix.data import list_class_names


def test_list_class_names_returns_sorted_classes(tmp_path: Path) -> None:
    split = tmp_path / "train"
    for class_name in ("warli", "gond"):
        class_dir = split / class_name
        class_dir.mkdir(parents=True)
        Image.new("RGB", (8, 8)).save(class_dir / "sample.jpg")

    assert list_class_names(split) == ["gond", "warli"]


def test_list_class_names_rejects_missing_split(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Dataset split directory not found"):
        list_class_names(tmp_path / "missing")


def test_list_class_names_rejects_class_without_images(tmp_path: Path) -> None:
    split = tmp_path / "train"
    (split / "gond").mkdir(parents=True)
    (split / "warli").mkdir()

    with pytest.raises(ValueError, match="No supported images"):
        list_class_names(split)
