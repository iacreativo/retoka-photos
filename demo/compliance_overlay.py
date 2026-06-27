"""
Visual compliance overlay for ID photos.

Draws the expected head zone and the actual head bounding box on the
final photo, so photographers can verify against official specs (ICAO, US Visa,
etc.) without opening Photoshop.

The overlay shows:
  - Cyan dashed rectangle: the EXPECTED head zone for the selected size
  - Green solid rectangle: the ACTUAL head bounding box (from face detection)
  - Status text: "OK" or "REVISAR" + head height percentage

For the source of every default value (ratio / head_height / top_distance) and
the math behind it, see ``docs/SIZE_SPECS.md``.

Usage:
    from demo.compliance_overlay import draw_compliance_overlay
    annotated = draw_compliance_overlay(image, face_bbox, expected_profile)
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# Compliance windows per standard. Each entry is (min_head_pct, max_head_pct)
# of the photo height the head (face + hair) should occupy.
#
# The thresholds and ranges were derived from official sources (ICAO 9303,
# US DS-160, SRE, SEDENA) — see ``docs/SIZE_SPECS.md`` for the full citation
# table and per-size calculation.
COMPLIANCE_STANDARDS = {
    "TIGHT": (0.80, 0.95),       # Infantil (face fills frame, no spec)
    "ICAO": (0.60, 0.85),        # Pasaporte MX, Cartilla, Visa MX (ICAO 9303)
    "US_VISA": (0.50, 0.70),     # Visa Americana (US DS-160: 49-69%)
    "SCHOOL": (0.45, 0.65),      # Óvalo, Diploma (school/credential style)
    "PORTRAIT": (0.30, 0.50),    # Título universitario (executive portrait)
}

# Multiplier from face-area-ratio to head-area-ratio.
# Hair typically adds ~30-35% above the face bounding box for the head top.
# face_h_fraction = sqrt(head_ratio), then we add hair allowance.
HAIR_VS_FACE_MULTIPLIER = 1.30


def _get_standard_for_size(head_ratio: float) -> str:
    """Pick the closest standard based on the configured head ratio.

    The actual head fraction (face + hair) in the final image is roughly
    sqrt(head_ratio) * HAIR_VS_FACE_MULTIPLIER. We classify based on this.
    """
    estimated_head = (head_ratio ** 0.5) * HAIR_VS_FACE_MULTIPLIER
    if estimated_head >= 0.80:
        return "TIGHT"
    if estimated_head >= 0.60:
        return "ICAO"
    if estimated_head >= 0.50:
        return "US_VISA"
    if estimated_head >= 0.45:
        return "SCHOOL"
    return "PORTRAIT"


def draw_compliance_overlay(
    pil_image: Image.Image,
    head_measure_ratio: float,
    head_height_ratio: float,
    top_distance: float,
    show_overlay: bool = True,
) -> Image.Image:
    """
    Draw a visual compliance overlay on the photo.

    Args:
        pil_image: PIL Image (the final cropped ID photo)
        head_measure_ratio: ratio that was used for cropping (face area / crop area)
        head_height_ratio: vertical position of face center
        top_distance: margin above the head
        show_overlay: if False, returns the image unchanged

    Returns:
        PIL Image with overlay drawn (or unchanged).

    Note: we don't need the source face bbox because the crop algorithm
    guarantees face_area / crop_area == head_measure_ratio. So face height
    fraction in the final image = sqrt(head_measure_ratio), and adding ~18%
    for hair gives the expected head height fraction.
    """
    if not show_overlay:
        return pil_image

    # Work in RGB space using PIL (better text rendering)
    img = pil_image.convert("RGB")
    w, h = img.size

    # Estimate the head height fraction in the final image
    face_h_fraction = (head_measure_ratio ** 0.5)
    head_h_fraction_with_hair = min(0.95, face_h_fraction * HAIR_VS_FACE_MULTIPLIER)

    # Draw the EXPECTED head zone as a dashed cyan rectangle
    expected_head_h_px = int(head_h_fraction_with_hair * h)
    expected_head_w_px = int(expected_head_h_px * 0.75)  # face width ~75% of height
    exp_x1 = (w - expected_head_w_px) // 2
    exp_x2 = exp_x1 + expected_head_w_px
    # Vertical: top margin = top_distance * photo height
    exp_y1 = int(top_distance * h)
    exp_y2 = exp_y1 + expected_head_h_px

    draw = ImageDraw.Draw(img, "RGBA")

    # Dashed cyan rectangle (expected zone)
    _draw_dashed_rect(draw, (exp_x1, exp_y1, exp_x2, exp_y2),
                       outline=(0, 200, 220, 255), width=2, dash=8, gap=4)

    # Choose the standard based on ratio
    standard = _get_standard_for_size(head_measure_ratio)
    min_pct, max_pct = COMPLIANCE_STANDARDS[standard]

    # Compute the actual head height percentage
    actual_pct = head_h_fraction_with_hair

    # Determine status
    if min_pct <= actual_pct <= max_pct:
        status = "OK"
        status_color = (40, 200, 80, 255)   # green
    elif actual_pct < min_pct:
        status = "Cara pequena"
        status_color = (255, 140, 0, 255)   # orange
    else:
        status = "Cara muy grande"
        status_color = (255, 60, 60, 255)   # red

    # Draw status banner at the top
    banner_h = 24
    draw.rectangle([(0, 0), (w, banner_h)], fill=(0, 0, 0, 210))
    # Try common Windows font paths; fall back to PIL default if unavailable.
    # On HF Spaces (Linux), these will fail and we use the default font (still readable).
    font_big = None
    font_small = None
    for path in (
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        try:
            font_big = ImageFont.truetype(path, 13)
            font_small = ImageFont.truetype(path, 10)
            break
        except OSError:
            continue
    if font_big is None:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    label = f"{standard} | Cabeza {actual_pct*100:.0f}% ({min_pct*100:.0f}-{max_pct*100:.0f}%) | {status}"
    draw.text((5, 4), label, fill=status_color, font=font_big)

    # Draw legend at the bottom
    legend_h = 16
    legend_y = h - legend_h
    draw.rectangle([(0, legend_y), (w, h)], fill=(0, 0, 0, 180))
    legend = f"Zona esperada de la cabeza | hr={head_measure_ratio:.2f} hh={head_height_ratio:.2f} td={top_distance:.2f}"
    draw.text((5, legend_y + 2), legend, fill=(220, 220, 220, 255), font=font_small)

    return img


def _draw_dashed_rect(draw, coords, outline, width=1, dash=6, gap=4):
    """Draw a dashed rectangle using PIL ImageDraw (no native support, so we
    draw short line segments)."""
    x1, y1, x2, y2 = coords
    # Top edge
    x = x1
    while x < x2:
        x_end = min(x + dash, x2)
        draw.line([(x, y1), (x_end, y1)], fill=outline, width=width)
        x += dash + gap
    # Bottom edge
    x = x1
    while x < x2:
        x_end = min(x + dash, x2)
        draw.line([(x, y2), (x_end, y2)], fill=outline, width=width)
        x += dash + gap
    # Left edge
    y = y1
    while y < y2:
        y_end = min(y + dash, y2)
        draw.line([(x1, y), (x1, y_end)], fill=outline, width=width)
        y += dash + gap
    # Right edge
    y = y1
    while y < y2:
        y_end = min(y + dash, y2)
        draw.line([(x2, y), (x2, y_end)], fill=outline, width=width)
        y += dash + gap