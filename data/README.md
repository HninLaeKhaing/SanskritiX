# Image dataset

The supplied `Indian Paintings Dataset.zip` contains 954 labeled image records in eight classes: `gond`, `kalighat`, `kangra`, `kerala`, `madhubani`, `mandana`, `pichwai`, and `warli`. This differs from the original five-class plan; the classifier uses the labels that are actually in the supplied dataset.

Prepare the ZIP into `data/images/{train,val,test}/<class-name>/` using a deterministic per-class 70/15/15 split:

```powershell
python -m sankritix.prepare_dataset
```

The preparation command resizes/canonicalizes images as 224x224 JPEG files and writes their source filename and dataset archive name into [`manifest.csv`](manifest.csv). It refuses to write into a non-empty output directory.

The ZIP includes an MIT license file, but that alone does not establish reuse rights for every artwork image inside it. Check the dataset's original source and image-level permissions before publishing, redistributing, or using the images outside this local experiment. The manifest marks image-specific terms as unverified.

The split is randomized by image, not by creator, source website, or original artwork. If the same artwork or near-duplicate is present more than once, it could appear in multiple splits and inflate test metrics. Review duplicates and provenance before treating evaluation results as reliable.

These visual categories are learning labels, not mutually exclusive cultural boundaries. Ask a knowledgeable reviewer to validate labels and document ambiguous cases; do not use the classifier to determine authenticity or provenance.
