"""main.py

Generate an LDraw model:
  - a 3x4 baseplate grid (12 baseplates)
  - a single centered digit "0" (as 1x1 plates)
  - the minifig template (optional)

Open the generated .ldr file in BrickLink Studio to preview.
"""

from pathlib import Path

from baseplate import build_baseplate_grid
from context import SceneContext
from digits import build_centered_digit
from minifig import build_minifig
from template import load_template, normalize_template_inplace

import math


def build_group(ctx, template, digit, center_stud_x, center_stud_z, color=15):

    lines = []

    # Center digit
    lines.extend(build_centered_digit(ctx, digit, center_stud_x, center_stud_z, color))

    # Fixed radius for all groups
    radius = 11

    # Place 10 minifigs evenly in a circle
    for i in range(10):
        angle = 2 * math.pi * i / 10

        fx = center_stud_x + radius * math.cos(angle)
        fz = center_stud_z + radius * math.sin(angle)

        lines.extend(
            build_minifig(
                ctx,
                template,
                stud_x=fx,
                stud_z=fz,
            )
        )

    return lines


def build_groups_grid(ctx, template, cols, rows, color=15):

    studs_per_plate = 32
    lines = []

    group_index = 1

    for r in range(rows):
        for c in range(cols):

            if group_index > 10:
                break

            # Special case: group 10 must be centered on last row
            if group_index == 10:
                center_x = (cols // 2) * studs_per_plate
                center_z = (rows - 1 - r) * studs_per_plate
            else:
                center_x = c * studs_per_plate
                center_z = (rows - 1 - r) * studs_per_plate

            lines.extend(
                build_group(
                    ctx,
                    template,
                    str(group_index),
                    center_x,
                    center_z,
                    color,
                )
            )

            group_index += 1

        if group_index > 10:
            break

    return lines


def main():
    project_dir = Path(__file__).parent
    build_dir = project_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    # Scene reference plane (kept for backward compatibility).
    ctx = SceneContext(ground_y=0)

    cols = 3
    rows = 5

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

    # 4) Add the minifig template (kept to preserve current output)
    template_path = project_dir / "template" / "minifig.ldr"
    tpl = load_template(template_path)
    normalize_template_inplace(tpl)

    lines.extend(
        build_groups_grid(
            ctx,
            tpl,
            cols=cols,
            rows=rows,
            color=15,
        )
    )

    # ---------------------------------------------------------------------
    # Export
    # ---------------------------------------------------------------------
    output_path = build_dir / "plateau_digits.ldr"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ File generated: {output_path}")


if __name__ == "__main__":
    main()
