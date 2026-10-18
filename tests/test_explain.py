import numpy as np
from PIL import Image
import tensorflow as tf

from sankritix.explain import gradcam_overlay


def test_gradcam_returns_rgb_overlay_for_convolutional_classifier() -> None:
    inputs = tf.keras.Input(shape=(224, 224, 3))
    augmentation = tf.keras.Sequential(
        [tf.keras.layers.RandomFlip("horizontal")],
        name="augmentation",
    )
    backbone_input = tf.keras.applications.mobilenet_v2.preprocess_input(
        augmentation(inputs)
    )
    backbone = tf.keras.Sequential(
        [
            tf.keras.layers.Conv2D(4, 3, padding="same", activation="relu"),
            tf.keras.layers.MaxPooling2D(),
        ],
        name="test_backbone",
    )
    x = backbone(backbone_input)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(2, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)

    overlay = gradcam_overlay(
        model,
        Image.fromarray(np.zeros((80, 120, 3), dtype=np.uint8)),
        class_index=0,
    )

    assert overlay.size == (224, 224)
    assert overlay.mode == "RGB"
