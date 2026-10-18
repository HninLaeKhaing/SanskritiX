from __future__ import annotations

import json
import csv
import hashlib
from pathlib import Path
from typing import TYPE_CHECKING
from datetime import datetime, timezone

from PIL import Image, UnidentifiedImageError
import streamlit as st

from sankritix.explain import gradcam_overlay
from sankritix.knowledge import TRADITIONS, quiz_questions, validate_traditions
from sankritix.predict import (
    assess_prediction,
    predict_image,
    rank_predictions,
)

if TYPE_CHECKING:
    import tensorflow as tf

ARTIFACTS_DIR = Path("artifacts")
MODEL_PATH = ARTIFACTS_DIR / "sankritix.keras"
CLASS_NAMES_PATH = ARTIFACTS_DIR / "class_names.json"
GUIDANCE_PATH = ARTIFACTS_DIR / "decision_guidance.json"
REPORT_PATH = ARTIFACTS_DIR / "test_report.json"
MANIFEST_PATH = Path("data/manifest.csv")
DATASET_ARCHIVE = Path("data/Indian Paintings Dataset.zip")

st.set_page_config(
    page_title="SanskritiX | Explore Indian Art",
    page_icon="🎨",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #25231f;
        --muted: #716a60;
        --paper: #f6f1e8;
        --surface: #fffdf8;
        --line: #e7dfd2;
        --terracotta: #a54f35;
        --green: #344d42;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 88% 4%, rgba(199, 166, 122, .15), transparent 28rem),
            var(--paper);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(246, 241, 232, .8); }
    [data-testid="stMainBlockContainer"] {
        max-width: 1160px;
        padding-top: 2.1rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3, h4 {
        color: var(--ink);
        letter-spacing: -.035em;
    }
    h2 { margin-top: 1.5rem; }
    p, label, li { color: #48443d; }
    [data-testid="stCaptionContainer"] p { color: var(--muted); }
    [data-testid="stTabs"] [role="tablist"] {
        gap: .45rem;
        border-bottom: 1px solid var(--line);
    }
    [data-testid="stTabs"] button[role="tab"] {
        border-radius: 999px 999px 0 0;
        padding: .72rem 1.1rem;
        font-weight: 600;
        color: var(--muted);
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: var(--terracotta);
    }
    [data-testid="stFileUploader"] section {
        background: rgba(255, 253, 248, .8);
        border: 1px dashed #c9bca8;
        border-radius: 18px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--line);
        border-radius: 18px;
        background: rgba(255, 253, 248, .68);
    }
    .hero-shell {
        display: grid;
        grid-template-columns: minmax(0, 1.12fr) minmax(320px, .88fr);
        align-items: center;
        gap: clamp(2rem, 6vw, 5rem);
        min-height: 390px;
        padding: clamp(1.7rem, 4vw, 3.6rem);
        margin: .3rem 0 2.6rem;
        overflow: hidden;
        border: 1px solid rgba(119, 93, 65, .16);
        border-radius: 28px;
        background:
            linear-gradient(112deg, rgba(255,253,248,.98) 0%, rgba(255,253,248,.92) 54%, rgba(239,229,211,.74) 100%);
        box-shadow: 0 22px 60px rgba(76, 58, 36, .08);
    }
    .hero-copy { position: relative; z-index: 1; }
    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: .6rem;
        color: var(--green);
        font-size: .72rem;
        font-weight: 750;
        letter-spacing: .15em;
        text-transform: uppercase;
    }
    .brand-name {
        display: block;
        margin-bottom: .75rem;
        color: var(--terracotta);
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: .015em;
    }
    .eyebrow::before {
        content: "";
        width: 26px;
        height: 1px;
        background: var(--terracotta);
    }
    .hero-title {
        max-width: 630px;
        margin: 1rem 0 .8rem;
        color: var(--ink);
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(3.1rem, 6.6vw, 5.4rem);
        font-weight: 500;
        letter-spacing: -.075em;
        line-height: .98;
    }
    .hero-title em {
        color: var(--terracotta);
        font-weight: 500;
    }
    .hero-description {
        max-width: 470px;
        color: #625b50;
        font-size: 1.03rem;
        line-height: 1.75;
    }
    .hero-meta {
        display: flex;
        flex-wrap: wrap;
        gap: .55rem;
        margin-top: 1.55rem;
    }
    .hero-meta span {
        padding: .45rem .78rem;
        border: 1px solid #e4d9c8;
        border-radius: 999px;
        background: rgba(255,255,255,.6);
        color: #544d43;
        font-size: .78rem;
    }
    .art-stage {
        position: relative;
        display: grid;
        min-height: 300px;
        place-items: center;
        perspective: 1000px;
        transform-style: preserve-3d;
    }
    .art-halo {
        position: absolute;
        width: min(23rem, 90%);
        aspect-ratio: 1;
        border: 1px solid rgba(165, 79, 53, .18);
        border-radius: 50%;
        box-shadow: 0 0 0 26px rgba(165,79,53,.035), 0 0 0 54px rgba(52,77,66,.025);
        transform: rotateX(62deg) rotateZ(-18deg);
    }
    .art-card {
        position: absolute;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: clamp(155px, 19vw, 220px);
        height: clamp(205px, 25vw, 275px);
        padding: 1rem;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,.48);
        border-radius: 9px;
        box-shadow: 0 28px 46px rgba(48, 38, 27, .25), inset 0 0 0 5px rgba(255,255,255,.12);
        transform-style: preserve-3d;
        transition: transform .35s ease, box-shadow .35s ease;
    }
    .art-card:hover {
        box-shadow: 0 38px 60px rgba(48, 38, 27, .31), inset 0 0 0 5px rgba(255,255,255,.12);
    }
    .art-card::before, .art-card::after {
        content: "";
        position: absolute;
        pointer-events: none;
    }
    .art-card::before {
        inset: 16% 13%;
        border: 1px solid rgba(255,255,255,.55);
        border-radius: 48% 48% 42% 42%;
        transform: translateZ(18px);
    }
    .art-card::after {
        width: 92px;
        height: 92px;
        top: 32%;
        left: 30%;
        border: 1px solid rgba(255,255,255,.65);
        border-radius: 50%;
        box-shadow: 0 0 0 12px rgba(255,255,255,.1), 0 0 0 25px rgba(255,255,255,.08);
        transform: translateZ(30px);
    }
    .art-card-one {
        z-index: 3;
        background:
            repeating-linear-gradient(135deg, transparent 0 13px, rgba(255,239,199,.2) 14px 15px),
            radial-gradient(ellipse at 55% 42%, #ce8a53 0 11%, transparent 12%),
            linear-gradient(145deg, #8e422e, #c36c42 52%, #d5a45e);
        transform: rotateY(-18deg) rotateX(5deg) rotateZ(-8deg) translateZ(35px);
    }
    .art-card-two {
        z-index: 2;
        background:
            repeating-radial-gradient(circle at 50% 45%, transparent 0 15px, rgba(245,229,188,.4) 16px 17px),
            linear-gradient(155deg, #334d43, #63745a 55%, #b28d5d);
        transform: rotateY(18deg) rotateX(3deg) rotateZ(9deg) translate3d(95px, 20px, -45px) scale(.88);
    }
    .art-card-three {
        z-index: 1;
        background:
            repeating-linear-gradient(0deg, transparent 0 17px, rgba(75,42,31,.2) 18px 19px),
            linear-gradient(150deg, #d8c29c, #b7885d 55%, #8d5943);
        transform: rotateY(-24deg) rotateX(-3deg) rotateZ(-19deg) translate3d(-92px, 36px, -95px) scale(.78);
    }
    .card-index, .card-name {
        position: relative;
        z-index: 2;
        color: #fff9eb;
        text-shadow: 0 1px 8px rgba(34,24,17,.28);
        transform: translateZ(42px);
    }
    .card-index {
        font-size: .62rem;
        font-weight: 700;
        letter-spacing: .18em;
    }
    .card-name {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.18rem;
    }
    .hero-footnote {
        position: absolute;
        right: 2%;
        bottom: 1%;
        color: #7a6f60;
        font-size: .66rem;
        letter-spacing: .12em;
        text-transform: uppercase;
    }
    .note {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid var(--line);
        border-radius: 1rem;
        padding: 1rem 1.2rem;
    }
    @media (max-width: 760px) {
        [data-testid="stMainBlockContainer"] { padding: 1rem 1rem 3rem; }
        .hero-shell {
            grid-template-columns: 1fr;
            gap: .5rem;
            padding: 1.6rem;
            margin-bottom: 1.6rem;
        }
        .art-stage { min-height: 265px; margin-top: .25rem; }
        .art-card-two { transform: rotateY(18deg) rotateX(3deg) rotateZ(9deg) translate3d(74px, 17px, -45px) scale(.84); }
        .art-card-three { transform: rotateY(-24deg) rotateX(-3deg) rotateZ(-19deg) translate3d(-72px, 30px, -95px) scale(.76); }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero-shell">
      <div class="hero-copy">
        <span class="brand-name">SanskritiX</span>
        <span class="eyebrow">A field guide to Indian art</span>
        <h1 class="hero-title">Look closer.<br><em>Learn the story.</em></h1>
        <p class="hero-description">
          Explore the visual languages, places, and living traditions behind
          India's art forms. Start with an image, then follow your curiosity.
        </p>
        <div class="hero-meta">
          <span>8 traditions</span><span>Image recognition</span><span>Made for curious minds</span>
        </div>
      </div>
      <div class="art-stage" aria-label="Layered three-dimensional abstract art cards">
        <div class="art-halo"></div>
        <div class="art-card art-card-three">
          <span class="card-index">FIELD NOTES · 03</span><span class="card-name">Living walls</span>
        </div>
        <div class="art-card art-card-two">
          <span class="card-index">FIELD NOTES · 02</span><span class="card-name">Patterns in place</span>
        </div>
        <div class="art-card art-card-one">
          <span class="card-index">FIELD NOTES · 01</span><span class="card-name">Stories in colour</span>
        </div>
        <span class="hero-footnote">A visual journey across India</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def load_model(model_path: str) -> tf.keras.Model:
    import tensorflow as tf

    return tf.keras.models.load_model(model_path)


def show_tradition_card(tradition_name: str) -> None:
    tradition = TRADITIONS[tradition_name]
    st.subheader(tradition["title"])
    st.markdown(f"**Region**  \n{tradition['region']}")
    st.markdown(f"**A short history**  \n{tradition['history']}")
    st.markdown(f"**Materials and making**  \n{tradition['materials']}")
    st.markdown(f"**What to notice**  \n{tradition['visual_language']}")
    st.markdown(f"**Cultural context**  \n{tradition['cultural_context']}")
    st.info(f"Look closely: {tradition['reflection']}")
    st.markdown("**Further reading**")
    for source_title, source_url in tradition["sources"]:
        st.markdown(f"- [{source_title}]({source_url})")
    st.caption(
        "These are introductory notes, not a complete history. Follow the "
        "references and consult artists, community knowledge holders, and "
        "museum or scholarly sources for deeper study."
    )


def show_identification_guide(
    tradition_name: str, alternative_name: str | None
) -> None:
    tradition = TRADITIONS[tradition_name]
    st.divider()
    st.subheader(f"Go beyond the label · {tradition['title']}")
    st.caption(
        "A short learning guide for this possible match. These are common "
        "features of the tradition, not claims that every feature appears "
        "in your specific image."
    )

    region_column, history_column = st.columns(2)
    with region_column:
        st.markdown("#### Place & tradition")
        st.write(tradition["region"])
        st.write(tradition["cultural_context"])
    with history_column:
        st.markdown("#### A little history")
        st.write(tradition["history"])
        st.caption(f"Materials: {tradition['materials']}")

    with st.container(border=True):
        st.markdown("#### Look closer")
        st.write(tradition["visual_language"])
        st.info(f"Try this: {tradition['reflection']}")

    if alternative_name is not None:
        alternative = TRADITIONS[alternative_name]
        with st.expander(
            f"Compare with another possible match: {alternative['title']}"
        ):
            first, second = st.columns(2)
            for column, match in ((first, tradition), (second, alternative)):
                with column:
                    st.markdown(f"#### {match['title']}")
                    st.caption(match["region"])
                    st.write(match["visual_language"])
                    st.caption(match["materials"])
            st.caption(
                "These are learning prompts, not evidence that one label is "
                "correct or that the other tradition is absent."
            )

    st.markdown("**Keep learning**")
    for source_title, source_url in tradition["sources"]:
        st.markdown(f"- [{source_title}]({source_url})")


def load_decision_guidance() -> tuple[dict[str, float | int | str], bool]:
    if GUIDANCE_PATH.is_file():
        guidance = json.loads(GUIDANCE_PATH.read_text(encoding="utf-8"))
        return guidance, True
    return (
        {
            "confidence_threshold": 0.55,
            "margin_threshold": 0.1,
            "method": "fixed_fallback_thresholds",
        },
        False,
    )


def show_dataset_transparency() -> None:
    st.markdown(
        "SanskritiX uses a labeled image archive for model training and a "
        "separate set of references for its learning notes."
    )
    if MANIFEST_PATH.is_file():
        with MANIFEST_PATH.open(newline="", encoding="utf-8") as manifest_file:
            rows = list(csv.DictReader(manifest_file))
        st.write(f"Training image records in the manifest: **{len(rows)}**")
        sources = sorted({row.get("source_dataset", "") for row in rows if row.get("source_dataset")})
        if sources:
            st.write("Dataset archive: " + ", ".join(sources))
        unverified = sum(
            "not verified" in row.get("license_or_permission", "").lower()
            for row in rows
        )
        if unverified:
            st.write(
                f"Image-level reuse terms marked unverified: **{unverified}**"
            )
    elif DATASET_ARCHIVE.is_file():
        st.write(f"Dataset archive found: **{DATASET_ARCHIVE.name}**")
    else:
        st.info("No dataset manifest or archive was found in the current project folder.")

    if REPORT_PATH.is_file():
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        accuracy = report.get("accuracy")
        if isinstance(accuracy, (int, float)):
            st.write(f"Held-out test accuracy recorded by this run: **{accuracy:.1%}**")

    st.warning(
        "The archive contains an MIT notice, but individual artwork reuse rights "
        "were not verified. Check image-level permissions before publishing or "
        "redistributing images or trained materials."
    )
    st.caption(
        "Dataset image labels come from the archive's class metadata. Cultural "
        "learning notes cite their own references and are introductory summaries, "
        "not community-reviewed or exhaustive histories."
    )


def record_discovery(
    filename: str,
    ranked: list[tuple[str, float]],
    image_digest: str,
) -> None:
    saved = st.session_state.saved_discoveries
    if any(item["image_id"] == image_digest for item in saved):
        st.info("This image is already in your saved discoveries.")
        return
    saved.append(
        {
            "image_id": image_digest,
            "filename": filename,
            "saved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "matches": [
                {"label": label, "score": round(score, 6)}
                for label, score in ranked
            ],
        }
    )
    st.success("Discovery saved for this browser session.")


if "saved_discoveries" not in st.session_state:
    st.session_state.saved_discoveries = []
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []
if "quiz_positions" not in st.session_state:
    st.session_state.quiz_positions = {}
if "quiz_feedback" not in st.session_state:
    st.session_state.quiz_feedback = {}
if "quiz_run_correct" not in st.session_state:
    st.session_state.quiz_run_correct = {}

identify_tab, learn_tab, quiz_tab = st.tabs(
    ["Identify artwork", "Explore traditions", "Knowledge check"]
)

with identify_tab:
    model_ready = MODEL_PATH.is_file() and CLASS_NAMES_PATH.is_file()
    model = None
    class_names: list[str] = []
    guidance: dict[str, float | int | str] = {
        "confidence_threshold": 0.55,
        "margin_threshold": 0.1,
        "method": "fixed_fallback_thresholds",
    }
    guidance_is_validation_based = False
    if model_ready:
        try:
            class_names = json.loads(CLASS_NAMES_PATH.read_text(encoding="utf-8"))
            validate_traditions(class_names)
            model = load_model(str(MODEL_PATH))
            guidance, guidance_is_validation_based = load_decision_guidance()
        except (OSError, ValueError, json.JSONDecodeError) as error:
            st.error(f"Could not load the trained model or its class labels: {error}")
    else:
        st.info(
            "Preview mode: the model is not trained yet, so photo classification "
            "is disabled. You can still explore the learning cards and quiz."
        )
        with st.container(border=True):
            st.caption("SAMPLE RESULT CARD · NOT GENERATED BY A MODEL")
            st.subheader("Madhubani")
            st.write("Illustrative class label")
            st.caption("After training, this area will show real model matches.")

    uploaded_image = st.file_uploader(
        "Choose an artwork image",
        type=("jpg", "jpeg", "png"),
        help="Use an image you have permission to upload.",
        disabled=model is None,
    )

    if model is not None and uploaded_image is not None:
        try:
            image = Image.open(uploaded_image)
            st.image(image, caption="Your image", use_container_width=True)
            ranked = rank_predictions(
                predict_image(model, image),
                class_names,
                top_k=3,
            )
        except (UnidentifiedImageError, OSError, ValueError) as error:
            st.error(f"Could not classify this image: {error}")
        else:
            best_name, best_score = ranked[0]
            is_uncertain, uncertainty_reason = assess_prediction(ranked, guidance)
            if is_uncertain:
                st.warning(
                    f"This is a tentative match: **{best_name}** ({best_score:.0%}). "
                    f"{uncertainty_reason} The correct style may not be among the "
                    "model's labels."
                )
            else:
                st.success(
                    f"Leading visual match: **{best_name}** ({best_score:.0%}). "
                    "Treat this as a suggestion, not a verified identification."
                )
            if guidance_is_validation_based:
                st.caption(
                    "Uncertainty guidance is based on a lower-percentile score "
                    "and top-match margin among correctly classified validation "
                    "images. It is a heuristic, not probability calibration."
                )
            else:
                st.caption(
                    "Validation-specific uncertainty guidance is unavailable; "
                    "the app is using fallback thresholds."
                )

            st.subheader("Other possible matches")
            for name, score in ranked:
                st.caption(f"{name} · {score:.0%}")
                st.progress(max(0.0, min(score, 1.0)))

            alternative_name = ranked[1][0] if len(ranked) > 1 else None
            show_identification_guide(best_name, alternative_name)

            st.subheader("Where the model looked")
            st.caption(
                "This attention map highlights image regions that influenced "
                "the model's score. It does not explain cultural meaning or prove "
                "that a highlighted feature identifies an art tradition."
            )
            if st.button("Generate attention map", key="generate_gradcam"):
                try:
                    attention = gradcam_overlay(
                        model,
                        image,
                        class_names.index(best_name),
                    )
                except (ValueError, RuntimeError) as error:
                    st.error(f"Could not generate the model attention map: {error}")
                else:
                    st.image(
                        attention,
                        caption="Grad-CAM attention overlay (exploratory only)",
                        use_container_width=True,
                    )

            image_digest = hashlib.sha256(uploaded_image.getvalue()).hexdigest()
            if st.button("Save this discovery", key="save_discovery"):
                record_discovery(uploaded_image.name, ranked, image_digest)

            st.caption(
                "Model scores compare visual patterns with the training labels. "
                "They do not prove an artwork's origin or authenticity."
            )
    elif model is not None:
        st.markdown(
            "Upload an image to see the model's closest matches. If traditions "
            "overlap or the photograph is unfamiliar, the right result may not "
            "be among this model's labels."
        )

with learn_tab:
    st.markdown(
        "Explore the traditions represented in the training dataset. "
        "Each guide introduces context and suggests questions for looking closely."
    )
    selected_tradition = st.selectbox(
        "Choose a tradition",
        options=list(TRADITIONS),
        format_func=lambda value: TRADITIONS[value]["title"],
        key="learning_tradition",
    )
    show_tradition_card(selected_tradition)

with quiz_tab:
    st.markdown(
        "Check what you noticed. These questions are for learning, not for "
        "judging the authenticity or cultural ownership of an artwork."
    )
    quiz_tradition = st.selectbox(
        "Choose a topic",
        options=list(TRADITIONS),
        format_func=lambda value: TRADITIONS[value]["title"],
        key="quiz_tradition",
    )
    questions = quiz_questions(quiz_tradition)
    question_index = st.session_state.quiz_positions.get(quiz_tradition, 0)
    feedback = st.session_state.quiz_feedback.get(quiz_tradition)
    progress_text = (
        "Quiz complete"
        if question_index >= len(questions)
        else f"Question {question_index + 1} of {len(questions)}"
    )
    st.progress(min(question_index / len(questions), 1.0), text=progress_text)

    if question_index >= len(questions):
        correct_in_quiz = st.session_state.quiz_run_correct.get(quiz_tradition, 0)
        st.success(
            f"Quiz complete! You got {correct_in_quiz} of {len(questions)} "
            "questions correct in this session."
        )
        if st.button("Play this quiz again", key=f"restart_{quiz_tradition}"):
            st.session_state.quiz_positions[quiz_tradition] = 0
            st.session_state.quiz_feedback.pop(quiz_tradition, None)
            st.session_state.quiz_run_correct[quiz_tradition] = 0
            st.rerun()
    else:
        question = questions[question_index]
        st.caption(
            f"{TRADITIONS[quiz_tradition]['title']} · "
            f"Question {question_index + 1}"
        )
        response = st.radio(
            question["prompt"],
            options=question["options"],
            index=None,
            key=f"answer_{quiz_tradition}_{question_index}",
            disabled=feedback is not None and feedback["index"] == question_index,
        )
        if feedback is not None and feedback["index"] == question_index:
            if feedback["correct"]:
                st.success(f"That's right. {question['explanation']}")
            else:
                st.warning(
                    f"Not quite. The best answer is **{question['answer']}**. "
                    f"{question['explanation']}"
                )
            if st.button(
                "Finish quiz" if question_index + 1 == len(questions) else "Next question",
                key=f"next_{quiz_tradition}_{question_index}",
            ):
                st.session_state.quiz_positions[quiz_tradition] = question_index + 1
                st.session_state.quiz_feedback.pop(quiz_tradition, None)
                st.rerun()
        elif st.button(
            "Check answer",
            key=f"check_{quiz_tradition}_{question_index}",
            disabled=response is None,
        ):
            is_correct = response == question["answer"]
            st.session_state.quiz_history.append(
                {"tradition": quiz_tradition, "correct": is_correct}
            )
            if is_correct:
                st.session_state.quiz_run_correct[quiz_tradition] = (
                    st.session_state.quiz_run_correct.get(quiz_tradition, 0) + 1
                )
            st.session_state.quiz_feedback[quiz_tradition] = {
                "index": question_index,
                "correct": is_correct,
            }
            st.rerun()

    attempts = st.session_state.quiz_history
    if attempts:
        correct_count = sum(item["correct"] for item in attempts)
        st.caption(
            f"Session learning progress: {correct_count} correct out of "
            f"{len(attempts)} answer checks."
        )

with st.expander("Dataset, sources, and responsible use"):
    show_dataset_transparency()

with st.expander(
    f"My saved discoveries ({len(st.session_state.saved_discoveries)})"
):
    if not st.session_state.saved_discoveries:
        st.caption(
            "Save a result from the Identify artwork tab. Saved records stay "
            "in this browser session; they do not contain the uploaded image."
        )
    else:
        for discovery in reversed(st.session_state.saved_discoveries):
            st.markdown(f"**{discovery['filename']}** · {discovery['saved_at']}")
            st.write(
                " · ".join(
                    f"{item['label']} ({item['score']:.0%})"
                    for item in discovery["matches"]
                )
            )
        st.download_button(
            "Download saved discoveries",
            data=json.dumps(st.session_state.saved_discoveries, indent=2),
            file_name="sankritix-discoveries.json",
            mime="application/json",
        )
        if st.button("Clear saved discoveries", key="clear_discoveries"):
            st.session_state.saved_discoveries = []
            st.rerun()
