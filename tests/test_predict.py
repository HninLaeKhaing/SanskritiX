import numpy as np
import pytest

from sankritix.predict import (
    assess_prediction,
    derive_decision_guidance,
    rank_predictions,
)


def test_rank_predictions_sorts_scores_and_limits_results() -> None:
    ranked = rank_predictions(
        np.array([0.2, 0.65, 0.15]),
        ["gond", "warli", "madhubani"],
        top_k=2,
    )

    assert ranked == [("warli", 0.65), ("gond", 0.2)]


def test_rank_predictions_rejects_class_count_mismatch() -> None:
    with pytest.raises(ValueError, match="must match the class names"):
        rank_predictions(np.array([0.8]), ["gond", "warli"])


def test_rank_predictions_rejects_non_finite_scores() -> None:
    with pytest.raises(ValueError, match="must all be finite"):
        rank_predictions(np.array([float("nan"), 0.2]), ["gond", "warli"])


def test_decision_guidance_uses_only_correct_validation_examples() -> None:
    labels = np.array([0, 1, 1, 0])
    scores = np.array(
        [
            [0.7, 0.3],
            [0.35, 0.65],
            [0.9, 0.1],
            [0.55, 0.45],
        ]
    )

    guidance = derive_decision_guidance(labels, scores)

    assert guidance["correct_validation_samples"] == 3
    assert guidance["confidence_threshold"] == pytest.approx(0.57)
    assert guidance["margin_threshold"] == pytest.approx(0.14)


def test_uncertainty_guidance_flags_close_top_matches() -> None:
    uncertain, reason = assess_prediction(
        [("gond", 0.51), ("warli", 0.47), ("mandana", 0.02)],
        {"confidence_threshold": 0.45, "margin_threshold": 0.1},
    )

    assert uncertain
    assert "two leading labels are close" in reason


def test_uncertainty_guidance_accepts_clearer_leading_match() -> None:
    uncertain, _ = assess_prediction(
        [("gond", 0.8), ("warli", 0.15), ("mandana", 0.05)],
        {"confidence_threshold": 0.6, "margin_threshold": 0.1},
    )

    assert not uncertain
