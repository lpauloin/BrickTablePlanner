"""digits.py

Render 5x7 "pixel" digits on a LEGO baseplate using 1x1 plates.

Each '#' character in the digit pattern corresponds to one 1x1 plate (3024.dat)
placed on a stud.

Coordinate conventions
----------------------
All placement functions take positions in *studs* (not LDraw units). Conversion
to LDraw units is done through the SceneContext.

The digits are defined as 7 rows (top to bottom) and 5 columns (left to right).
When mapping to the baseplate grid:

  - Increasing X moves to the right.
  - Increasing Z moves "down" the digit (towards later rows).

Because different viewers/tools may interpret the camera orientation
differently, we explicitly flip the digit vertically when placing studs so that
row 0 of the pattern is visually at the top in BrickLink Studio.
"""

from context import PLATE_HEIGHT

PLATE_1x1 = "3024.dat"


# Digits: 5x7 pixel patterns, '#' = stud occupied by a 1x1 plate
DIGITS_5x7 = {
    "1": [
        "..#..",
        ".##..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
    ],
    "2": [
        ".###.",
        "#...#",
        "....#",
        "..##.",
        ".#...",
        "#....",
        "#####",
    ],
    "3": [
        "####.",
        "....#",
        "..##.",
        "....#",
        "....#",
        "#...#",
        ".###.",
    ],
    "4": [
        "#..#.",
        "#..#.",
        "#..#.",
        "#####",
        "...#.",
        "...#.",
        "...#.",
    ],
    "5": [
        "#####",
        "#....",
        "####.",
        "....#",
        "....#",
        "#...#",
        ".###.",
    ],
    "6": [
        ".###.",
        "#....",
        "####.",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ],
    "7": [
        "#####",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#....",
    ],
    "8": [
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        "#...#",
        "#...#",
        ".###.",
    ],
    "9": [
        ".###.",
        "#...#",
        "#...#",
        ".####",
        "....#",
        "...#.",
        ".##..",
    ],
    "0": [
        ".###.",
        "#...#",
        "#..##",
        "#.#.#",
        "##..#",
        "#...#",
        ".###.",
    ],
}


def render_text_5x7(text, gap=1):
    """Build a 5x7 matrix (list of strings) from a string of digits."""

    if not text:
        raise ValueError("Empty text")

    for ch in text:
        if ch not in DIGITS_5x7:
            raise ValueError(f"Unsupported character: {ch!r}")

    height = 7
    rows = [""] * height

    for i, ch in enumerate(text):
        digit = DIGITS_5x7[ch]
        for r in range(height):
            rows[r] += digit[r]
        if i < len(text) - 1:
            for r in range(height):
                rows[r] += "." * gap

    return rows


def build_centered_digit(ctx, text, center_stud_x, center_stud_z, color=15):
    """
    Render a digit (or multi-digit string) centered at a given stud position.

    Parameters
    ----------
    ctx : SceneContext
        Scene coordinate system helper (LDUs conversion, baseplate height, etc.).
    text : str
        Digit string to render (e.g. "1", "10").
    center_stud_x : float
        X coordinate of the desired center in stud space.
    center_stud_z : float
        Z coordinate of the desired center in stud space.
    color : int
        LDraw color code for the plates.

    Notes
    -----
    - The digit is defined as a 5x7 bitmap.
    - Stud coordinates are integer-aligned.
    - Baseplates are centered on half-stud offsets in the scene.
      Therefore, a +0.5 stud correction is applied to ensure proper alignment
      with the physical stud grid.
    """

    # Generate the 5x7 bitmap matrix (list of strings)
    matrix = render_text_5x7(text)

    height = len(matrix)  # number of rows (typically 7)
    width = len(matrix[0])  # number of columns (typically 5 per digit)

    # ---------------------------------------------------------------------
    # Stud grid alignment correction
    #
    # Baseplates are positioned by their geometric center.
    # However, LEGO studs are positioned on integer coordinates.
    #
    # A half-stud offset ensures the bitmap aligns exactly on the stud grid.
    # ---------------------------------------------------------------------
    half_stud = 0.5

    # Compute the top-left origin of the bitmap in stud space.
    # (width - 1)/2 and (height - 1)/2 give the exact pixel center.
    origin_x = center_stud_x - (width - 1) / 2 + half_stud
    origin_z = center_stud_z - (height - 1) / 2 + half_stud

    lines = []

    # Iterate through the bitmap
    for row_idx, row in enumerate(matrix):
        for col_idx, pixel in enumerate(row):

            # Only place plates where the bitmap contains a filled pixel
            if pixel != "#":
                continue

            # Compute stud position of this pixel
            stud_x = origin_x + col_idx

            # Vertical inversion: bitmap row 0 is top visually,
            # but increasing Z moves "up" in the scene.
            stud_z = origin_z + (height - 1 - row_idx)

            # Convert stud coordinates to LDraw units (LDUs)
            x = ctx.studs(stud_x)
            z = ctx.studs(stud_z)

            # Plates sit exactly on top of the baseplate surface
            y = ctx.baseplate_top_origin_y

            # Emit LDraw Type-1 line (1x1 plate)
            lines.append(
                f"1 {color} {x:.6f} {y:.6f} {z:.6f} 1 0 0 0 1 0 0 0 1 {PLATE_1x1}"
            )

    return lines
