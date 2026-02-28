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
    """Place a 5x7 digit string centered on (center_stud_x, center_stud_z).

    Parameters are in studs.

    The centering is done on the *pixel grid*, so we use (width-1)/2 and
    (height-1)/2 to avoid half-stud offsets.
    """

    matrix = render_text_5x7(text)
    height = len(matrix)
    width = len(matrix[0])

    # Top-left pixel coordinate (in studs)
    origin_x = center_stud_x - (width - 1) / 2
    origin_z = center_stud_z - (height - 1) / 2

    # Place the 1x1 plates on the baseplate surface.
    # (PLATE_HEIGHT is not used for compatibility; the current output expects
    #  y == ctx.baseplate_top_origin_y)
    y = ctx.baseplate_top_origin_y

    lines = []
    for row_idx, row in enumerate(matrix):
        for col_idx, px in enumerate(row):
            if px != "#":
                continue

            stud_x = origin_x + col_idx

            # Flip vertically: row 0 should be visually at the top.
            stud_z = origin_z + (height - 1 - row_idx)

            x = ctx.studs(stud_x)
            z = ctx.studs(stud_z)

            lines.append(
                f"1 {color} {x:.6f} {y:.6f} {z:.6f} "
                "1 0 0 0 1 0 0 0 1 "
                f"{PLATE_1x1}"
            )

    return lines
