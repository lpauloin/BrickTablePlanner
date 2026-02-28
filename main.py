from pathlib import Path
from context import SceneContext
from baseplate import build_baseplate_grid
from digits import build_centered_digit, build_digit_grid
from minifig import build_minifig, load_minifig_template


def main():
    project_dir = Path(__file__).parent

    template_path = project_dir / "template" / "minifig.ldr"

    build_path = project_dir / "build"
    build_path.mkdir(parents=True, exist_ok=True)

    ctx = SceneContext(ground_y=0)

    lines = []
    lines.append("0 Plateau + digits test")
    lines.append("0 Name:  Untitled Model")
    lines.append("0 Author:  ")
    lines.append("0 CustomBrick")
    lines.append("0 FlexibleBrickControlPointUnitLength -1")
    lines.append("0 FlexibleBrickLockedControlPoint ")
    lines.append("0")

    cols = 3
    rows = 4
    studs_per_plate = 32
    center_stud_x = (cols * studs_per_plate) / 2
    center_stud_z = (rows * studs_per_plate) / 2
    center_stud_z = center_stud_z / 2

    lines.extend(build_baseplate_grid(ctx, cols=cols, rows=rows, color=1))

    lines.extend(
        build_centered_digit(
            ctx,
            "0",
            center_stud_x=center_stud_z,
            center_stud_z=center_stud_x,
            color=15,
        )
    )

    tpl = load_minifig_template(template_path)
    lines.extend(
        build_minifig(
            ctx,
            tpl,
            stud_x=center_stud_z,
            stud_z=center_stud_x,
        )
    )

    output_path = build_path / "plateau_digits.ldr"
    output_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"✅ File generated: {output_path}")


if __name__ == "__main__":
    main()
