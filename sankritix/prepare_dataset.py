import argparse
import csv
import io
import random
from collections import defaultdict
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

from PIL import Image, UnidentifiedImageError

IMAGE_SIZE = (224, 224)
SPLIT_RATIOS = (("train", 0.7), ("val", 0.15))


def split_by_class(
    rows: list[dict[str, str]], seed: int
) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["class"]].append(row)

    split_rows: dict[str, list[dict[str, str]]] = {
        "train": [],
        "val": [],
        "test": [],
    }
    for class_rows in grouped.values():
        class_rows.sort(key=lambda row: row["image"])
        random.Random(seed + sum(ord(char) for char in class_rows[0]["class"])).shuffle(
            class_rows
        )
        train_end = int(len(class_rows) * SPLIT_RATIOS[0][1])
        val_end = train_end + int(len(class_rows) * SPLIT_RATIOS[1][1])
        split_rows["train"].extend(class_rows[:train_end])
        split_rows["val"].extend(class_rows[train_end:val_end])
        split_rows["test"].extend(class_rows[val_end:])

    return split_rows


def prepare_dataset(archive_path: Path, output_dir: Path, seed: int) -> None:
    if not archive_path.is_file():
        raise FileNotFoundError(f"Dataset archive not found: {archive_path}")
    if output_dir.exists() and any(path.is_file() for path in output_dir.rglob("*")):
        raise FileExistsError(
            f"Output directory is not empty: {output_dir}. "
            "Move or remove its contents before preparing the dataset."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir.parent / "manifest.csv"

    try:
        with ZipFile(archive_path) as archive:
            with archive.open("classes.csv") as class_file:
                rows = list(
                    csv.DictReader(io.TextIOWrapper(class_file, encoding="utf-8"))
                )
            if not rows or not {"image", "class"}.issubset(rows[0]):
                raise ValueError("Archive classes.csv must contain image and class columns.")

            referenced_images = {row["image"] for row in rows}
            names_by_basename: dict[str, str] = {}
            for name in archive.namelist():
                if name.endswith("/"):
                    continue
                basename = PurePosixPath(name).name
                if basename not in referenced_images:
                    continue
                if basename in names_by_basename:
                    raise ValueError(
                        f"Duplicate image filename in archive: {basename}"
                    )
                names_by_basename[basename] = name

            if len(rows) < 3:
                raise ValueError("Dataset needs at least three labeled images.")
            for row in rows:
                if row["image"] not in names_by_basename:
                    raise ValueError(
                        f"Image listed in classes.csv is missing: {row['image']}"
                    )

            split_rows = split_by_class(rows, seed)
            with manifest_path.open("w", newline="", encoding="utf-8") as manifest_file:
                writer = csv.DictWriter(
                    manifest_file,
                    fieldnames=[
                        "split",
                        "path",
                        "label",
                        "source_dataset",
                        "source_url",
                        "creator",
                        "license_or_permission",
                        "reviewed_by",
                        "notes",
                    ],
                )
                writer.writeheader()
                for split, split_class_rows in split_rows.items():
                    for index, row in enumerate(split_class_rows):
                        relative_path = Path(split) / row["class"] / f"{index:05d}.jpg"
                        destination = output_dir / relative_path
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        try:
                            with Image.open(
                                io.BytesIO(archive.read(names_by_basename[row["image"]]))
                            ) as image:
                                image.convert("RGB").resize(IMAGE_SIZE).save(
                                    destination,
                                    format="JPEG",
                                    quality=90,
                                    optimize=True,
                                )
                        except (UnidentifiedImageError, OSError) as error:
                            raise ValueError(
                                f"Could not process {row['image']}: {error}"
                            ) from error

                        writer.writerow(
                            {
                                "split": split,
                                "path": relative_path.as_posix(),
                                "label": row["class"],
                                "source_dataset": archive_path.name,
                                "source_url": "",
                                "creator": "",
                                "license_or_permission": (
                                    "Archive includes MIT LICENSE; individual "
                                    "artwork reuse terms not verified"
                                ),
                                "reviewed_by": "",
                                "notes": f"Original archive image: {row['image']}",
                            }
                        )
    except BadZipFile as error:
        raise ValueError(f"Not a valid ZIP archive: {archive_path}") from error

    class_counts = {
        split: len(split_class_rows) for split, split_class_rows in split_rows.items()
    }
    print(f"Prepared {len(rows)} images into {output_dir}: {class_counts}")
    print(f"Recorded source metadata in {manifest_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare labeled images from the supplied paintings ZIP archive."
    )
    parser.add_argument(
        "--archive",
        type=Path,
        default=Path("data/Indian Paintings Dataset.zip"),
    )
    parser.add_argument("--output-dir", type=Path, default=Path("data/images"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    prepare_dataset(args.archive, args.output_dir, args.seed)


if __name__ == "__main__":
    main()
