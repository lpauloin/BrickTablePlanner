def build_minifig(ctx, template, stud_x, stud_z):
    dx = ctx.studs(stud_x)
    dz = ctx.studs(stud_z)
    dy = ctx.baseplate_top_origin_y

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
