from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from PIL import Image

from sankritix.config import IMAGE_SIZE

if TYPE_CHECKING:
    import tensorflow as tf


def gradcam_overlay(
    model: tf.keras.Model,
    image: Image.Image,
    class_index: int,
) -> Image.Image:
    import tensorflow as tf

    backbones = [
        layer
        for layer in model.layers
        if isinstance(layer, tf.keras.Model)
        and any(
            isinstance(nested, tf.keras.layers.Conv2D)
            for nested in layer.layers
        )
    ]
    if not backbones:
        raise ValueError("Grad-CAM requires a model with a convolutional backbone.")
    if class_index < 0 or class_index >= int(model.output_shape[-1]):
        raise ValueError("class_index is outside the model's output range.")

    backbone = backbones[-1]
    resized = image.convert("RGB").resize(IMAGE_SIZE)
    pixels = np.asarray(resized, dtype=np.float32)[None, ...]

    with tf.GradientTape() as tape:
        inputs = tf.convert_to_tensor(pixels)
        x = model.layers[1](inputs, training=False)
        x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
        feature_maps = backbone(x, training=False)
        tape.watch(feature_maps)
        x = feature_maps
        backbone_index = model.layers.index(backbone)
        for layer in model.layers[backbone_index + 1 :]:
            x = layer(x, training=False)
        predictions = x
        class_score = predictions[:, class_index]
    gradients = tape.gradient(class_score, feature_maps)
    if gradients is None:
        raise ValueError("Could not compute Grad-CAM gradients for this model.")

    weights = tf.reduce_mean(gradients, axis=(1, 2), keepdims=True)
    heatmap = tf.reduce_sum(weights * feature_maps, axis=-1)[0]
    heatmap = tf.maximum(heatmap, 0)
    maximum = tf.reduce_max(heatmap)
    if float(maximum.numpy()) > 0:
        heatmap = heatmap / maximum

    heatmap_image = Image.fromarray(
        np.uint8(255 * heatmap.numpy())
    ).resize(IMAGE_SIZE, Image.Resampling.BILINEAR)
    heat = np.asarray(heatmap_image, dtype=np.float32) / 255
    color_map = np.stack(
        [
            np.full_like(heat, 255),
            np.clip(heat * 190, 0, 255),
            np.zeros_like(heat),
        ],
        axis=-1,
    ).astype(np.uint8)
    overlay = Image.blend(resized, Image.fromarray(color_map), alpha=0.35)
    return overlay
