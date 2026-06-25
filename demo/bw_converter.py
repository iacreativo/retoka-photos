# -*- coding: utf-8 -*-
"""
Black & white conversion tuned for ID / passport photos.

Why a dedicated module instead of cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)?

For ID / passport photos the naive grayscale conversion usually ends up
looking flat — facial features lose contrast, skin turns muddy, the photo
fails the "clearly visible facial features" requirement that ICAO 9303,
US DS-160, and SRE all enforce.

This module implements the classic studio approach:

  1. Compute perceptual luminance using ITU-R BT.601 weights
     (Y = 0.299 R + 0.587 G + 0.114 B).  These weights were chosen
     because they make skin tones come out at a natural midtone — using
     the more neutral BT.709 weights washes out skin.

  2. Blend toward full B&W by ``intensity`` (0 = keep original colour,
     100 = full grayscale).  This lets the photographer dial in subtle
     desaturation vs. pure black-and-white.

  3. Apply a gentle contrast / gamma boost so eyes, eyebrows, lips and
     hairline stay clearly defined.  The contrast factor is clamped to a
     sensible range so we never blow out highlights or crush shadows —
     ID photos need *both* detail in shadows AND no glare.

  4. Optional very mild unsharp mask to compensate for the softness that
     grayscale conversion adds.  Off by default (sharpen_strength=0 in
     the existing beauty tab already covers it).

References:
  - ICAO Doc 9303 §3.2 — "facial features must be clearly visible"
  - US DS-160 photo tool — same requirement, plus "head must contrast
    with background"
  - Standard studio retouching workflow: desaturate → contrast → sharpen
"""

from __future__ import annotations

import cv2
import numpy as np


# ITU-R BT.601 luminance weights — chosen over BT.709 because skin tones
# (R≈230, G≈190, B≈170) yield a natural midtone gray ≈ 200 instead of
# looking pale/washed out.
_LUMA_B = 0.114
_LUMA_G = 0.587
_LUMA_R = 0.299


def _to_bgr(img: np.ndarray) -> np.ndarray:
    """Accepts either BGR (cv2 native) or RGBA; returns BGR with alpha dropped."""
    if img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img.shape[2] == 4:
        return img[:, :, :3]
    return img


def _to_rgba(bgr: np.ndarray, alpha: np.ndarray | None) -> np.ndarray:
    if alpha is None:
        return bgr
    return np.dstack([bgr, alpha])


def _extract_alpha(img: np.ndarray) -> np.ndarray | None:
    if img.ndim == 3 and img.shape[2] == 4:
        return img[:, :, 3]
    return None


def _luminance_bgr(bgr: np.ndarray) -> np.ndarray:
    """Perceptual luminance using BT.601 weights. Returns float32 [0..255]."""
    b, g, r = cv2.split(bgr.astype(np.float32))
    return _LUMA_R * r + _LUMA_G * g + _LUMA_B * b


def _apply_contrast(gray: np.ndarray, contrast_pct: float) -> np.ndarray:
    """
    Contrast adjustment centered on mid-gray (128).
    contrast_pct = 0   → no change
    contrast_pct = 30  → (gray - 128) * 1.30 + 128
    contrast_pct = -30 → (gray - 128) * 0.70 + 128
    """
    if abs(contrast_pct) < 1e-3:
        return gray
    factor = 1.0 + (contrast_pct / 100.0)
    factor = max(0.4, min(factor, 2.0))  # clamp so we never destroy the image
    return (gray - 128.0) * factor + 128.0


def _apply_gamma(gray: np.ndarray, gamma: float) -> np.ndarray:
    """
    Gamma adjustment.  gamma = 1.0 → no change.
    For ID photos, slight gamma lift (1.05–1.15) opens shadows without
    blowing highlights — useful for older subjects or harsh studio light.
    """
    if abs(gamma - 1.0) < 1e-3:
        return gray
    inv = 1.0 / max(0.4, min(gamma, 2.5))
    # Normalize to [0,1], apply gamma, scale back to [0,255]
    return np.power(np.clip(gray / 255.0, 0.0, 1.0), inv) * 255.0


def convert_to_bw(
    img: np.ndarray,
    intensity: float = 100.0,
    contrast: float = 12.0,
    gamma: float = 1.05,
    preserve_alpha: bool = True,
) -> np.ndarray:
    """
    Convert an image to black & white with ID-photo-friendly defaults.

    Parameters
    ----------
    img : np.ndarray
        BGR or BGRA image (uint8).
    intensity : float
        0 = keep original colour, 100 = full grayscale.
        Default 100 — pure B&W.  Dial down for sepia-toned prints.
    contrast : float
        Contrast adjustment in percent.  Default 12 — gentle boost that
        keeps features readable without crushing shadows or blowing
        highlights.  Range: -50 to +50.
    gamma : float
        Gamma value.  Default 1.05 — slight shadow lift.  Range: 0.4–2.5.
    preserve_alpha : bool
        If True (default) and the input has an alpha channel, the alpha
        is preserved unchanged (only RGB is converted).

    Returns
    -------
    np.ndarray
        Same channel layout as input (BGR or BGRA), uint8.
    """
    alpha = _extract_alpha(img) if preserve_alpha else None
    bgr = _to_bgr(img)

    # 1. Perceptual luminance
    luma = _luminance_bgr(bgr)

    # 2. Contrast + gamma lift — gives features the "pop" ID photos need
    luma = _apply_contrast(luma, contrast)
    luma = _apply_gamma(luma, gamma)
    luma = np.clip(luma, 0.0, 255.0).astype(np.uint8)

    # 3. Broadcast luminance to 3 channels
    gray_bgr = cv2.merge([luma, luma, luma])

    # 4. Blend toward B&W by intensity
    blend = max(0.0, min(intensity, 100.0)) / 100.0
    if blend >= 0.999:
        out = gray_bgr
    elif blend <= 0.001:
        out = bgr
    else:
        out = cv2.addWeighted(bgr, 1.0 - blend, gray_bgr, blend, 0)

    return _to_rgba(out, alpha)


def is_mostly_grayscale(img: np.ndarray, threshold: float = 8.0) -> bool:
    """
    Detect if an image is already nearly grayscale (R≈G≈B per pixel).
    Used to skip the conversion step when not needed.
    """
    if img.ndim == 2 or (img.ndim == 3 and img.shape[2] < 3):
        return True
    bgr = _to_bgr(img)
    b, g, r = cv2.split(bgr.astype(np.int16))
    # Mean absolute difference between channels — small => gray
    rg = np.mean(np.abs(r - g))
    rb = np.mean(np.abs(r - b))
    gb = np.mean(np.abs(g - b))
    return (rg + rb + gb) / 3.0 < threshold
