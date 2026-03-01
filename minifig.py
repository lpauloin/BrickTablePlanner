from context import BASEPLATE_THICKNESS


def build_minifig(ctx, template, stud_x, stud_z):
    """
    Place a normalized minifig template at the given stud position.

    Assumptions:
    - Template is already normalized
    - Template Y=0 corresponds to ground reference
    - No rotation applied
    """

    dx = ctx.studs(stud_x)
    dz = ctx.studs(stud_z)
    dy = ctx.ground_y - BASEPLATE_THICKNESS  # just snap to plate

    out = []

    for p in template:

        final_x = p.x + dx
        final_y = p.y + dy
        final_z = p.z + dz

        out.append(
            f"1 {p.color} {final_x} {final_y} {final_z} "
            f"{p.a} {p.b} {p.c} {p.d} {p.e} {p.f} {p.g} {p.h} {p.i} "
            f"{p.part_id}"
        )

    return out
