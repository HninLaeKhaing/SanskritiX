import pytest

from sankritix.knowledge import TRADITIONS, quiz_questions, validate_traditions


def test_every_training_label_has_learning_content() -> None:
    validate_traditions(
        [
            "gond",
            "kalighat",
            "kangra",
            "kerala",
            "madhubani",
            "mandana",
            "pichwai",
            "warli",
        ]
    )


def test_learning_cards_include_context_sources_and_quiz() -> None:
    for tradition in TRADITIONS.values():
        assert tradition["region"]
        assert tradition["history"]
        assert tradition["materials"]
        assert tradition["visual_language"]
        assert tradition["cultural_context"]
        assert tradition["sources"]
        assert all(url.startswith("https://") for _, url in tradition["sources"])
        assert tradition["question"]["answer"] in tradition["question"]["options"]


def test_every_tradition_has_three_valid_quiz_questions() -> None:
    for tradition_name in TRADITIONS:
        questions = quiz_questions(tradition_name)
        assert len(questions) == 3
        for question in questions:
            assert question["prompt"]
            assert question["answer"] in question["options"]
            assert question["explanation"]


def test_unknown_model_label_has_explicit_error() -> None:
    with pytest.raises(ValueError, match="No learning content is available"):
        validate_traditions(["unlisted-tradition"])
