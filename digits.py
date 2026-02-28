from __future__ import annotations

from typing import Dict, List

PLATE_1x1 = "3024.dat"

# Digits: 5x7 pixel patterns, '#' = stud occupied by a 1x1 plate
DIGITS_5x7: Dict[str, List[str]] = {
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


def render_text_5x7(text: str, gap: int = 1):
    """
    Build a 5x7 pixel matrix from a string of digits.
    Supports any length (e.g. "10", "123", etc).

    Returns a list of strings (rows), same format as DIGITS_5x7.
    """

    if not text:
        raise ValueError("Empty text")

    # Validate characters
    for ch in text:
        if ch not in DIGITS_5x7:
            raise ValueError(f"Unsupported character: {ch}")

    height = 7
    result = [""] * height

    for i, ch in enumerate(text):
        digit = DIGITS_5x7[ch]

        for row in range(height):
            result[row] += digit[row]

        # Add spacing between digits (except after last)
        if i < len(text) - 1:
            for row in range(height):
                result[row] += "." * gap

    return result


def build_centered_digit(ctx, text, center_stud_x, center_stud_z, color=15):

    matrix = render_text_5x7(text)

    height = len(matrix)
    width = len(matrix[0])

    origin_x = center_stud_x - (width - 1) / 2
    origin_z = center_stud_z - (height - 1) / 2

    lines = []

    for row_idx, row in enumerate(matrix):
        for col_idx, px in enumerate(row):

            if px != "#":
                continue

            stud_x = origin_x + col_idx
            stud_z = origin_z + (height - 1 - row_idx)

            # ✅ PAS de swap
            x = ctx.studs(stud_x)
            z = ctx.studs(stud_z)

            y = ctx.baseplate_top_origin_y

            lines.append(
                f"1 {color} {x:.6f} {y:.6f} {z:.6f} " "1 0 0 0 1 0 0 0 1 3024.dat"
            )

    return lines


def build_digit_grid(ctx, cols, rows, digits, color=15):
    """
    Place digits evenly distributed across baseplate grid.

    - cols / rows = number of baseplates
    - digits = list of strings (["1","2","3",...])
    """

    studs_per_plate = 32

    total_width = cols * studs_per_plate
    total_depth = rows * studs_per_plate

    cells_per_row = 3
    cell_width = total_width / cells_per_row
    cell_depth = total_depth / 4  # 4 rows of digits

    lines = []

    for index, digit in enumerate(digits):

        grid_row = index // 3
        grid_col = index % 3

        if digit == "10":
            grid_col = 1  # center bottom

        center_stud_x = (grid_col + 0.5) * cell_width
        center_stud_z = (grid_row + 0.5) * cell_depth

        lines.extend(
            build_centered_digit(ctx, digit, center_stud_x, center_stud_z, color)
        )

    return lines
