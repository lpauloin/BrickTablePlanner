"""main.py

Generate an LDraw model:
  - a 3x4 baseplate grid (12 baseplates)
  - a single centered digit "0" (as 1x1 plates)
  - the minifig template (optional)

Open the generated .ldr file in BrickLink Studio to preview.
"""

from pathlib import Path

from baseplate import build_baseplate_grid
from context import SceneContext, grid_center_in_studs
from digits import build_centered_digit
from minifig import build_minifig, load_minifig_template


def build_digits_1_to_10(ctx, cols, rows, color=15):

    studs_per_plate = 32
    lines = []

    # Logical grid 4 rows x 3 columns
    for i in range(10):

        digit = str(i + 1)

        if i < 9:
            logical_row = i // 3  # 0,1,2
            logical_col = i % 3  # 0,1,2
        else:
            # 10 centered on last row
            logical_row = 3
            logical_col = 1  # middle column

        center_x = logical_col * studs_per_plate

        # invert vertical axis properly
        center_z = (rows - 1 - logical_row) * studs_per_plate

        lines.extend(build_centered_digit(ctx, digit, center_x, center_z, color))

    return lines


def main():
    project_dir = Path(__file__).parent
    build_dir = project_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    # Scene reference plane (kept for backward compatibility).
    ctx = SceneContext(ground_y=0)

    cols = 3
    rows = 4

    # ---------------------------------------------------------------------
    # Build model
    # ---------------------------------------------------------------------

    lines = [
        "0 Plateau + digits test",
        "0 Name:  Untitled Model",
        "0 Author:  ",
        "0 CustomBrick",
        "0 FlexibleBrickControlPointUnitLength -1",
        "0 FlexibleBrickLockedControlPoint ",
        "0",
    ]

    # 1) Baseplate grid (each 3811.dat is 32x32 studs)
    lines.extend(build_baseplate_grid(ctx, cols=cols, rows=rows, color=1))

    # 2) Compute the *true* grid center (in studs)
    #    Note: baseplates are placed by *center*, so the grid center is not
    #    simply (total_studs / 2).
    center_stud_x, center_stud_z = grid_center_in_studs(cols, rows)

    # 3) Add a single centered digit
    # lines.extend(build_centered_digit(ctx, "0", center_stud_x, center_stud_z, color=15))
    lines.extend(build_digits_1_to_10(ctx, cols, rows, color=15))

    # 4) Add the minifig template (kept to preserve current output)
    template_path = project_dir / "template" / "minifig.ldr"
    tpl = load_minifig_template(template_path)
    lines.extend(build_minifig(ctx, tpl, stud_x=center_stud_x, stud_z=center_stud_z))

    # ---------------------------------------------------------------------
    # Export
    # ---------------------------------------------------------------------
    output_path = build_dir / "plateau_digits.ldr"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ File generated: {output_path}")


if __name__ == "__main__":
    main()
