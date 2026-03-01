PLATES = {
    1: {
        1: "3024.dat",  # Plate 1 x 1
        2: "3023.dat",  # Plate 1 x 2
        3: "3623.dat",  # Plate 1 x 3
        4: "3710.dat",  # Plate 1 x 4
        6: "3666.dat",  # Plate 1 x 6
        8: "3460.dat",  # Plate 1 x 8
        10: "4477.dat",  # Plate 1 x 10
        12: "60479.dat",  # Plate 1 x 12
    },
    2: {
        2: "3022.dat",  # Plate 2 x 2
        3: "3021.dat",  # Plate 2 x 3
        4: "3020.dat",  # Plate 2 x 4
        6: "3795.dat",  # Plate 2 x 6
        8: "3034.dat",  # Plate 2 x 8
        10: "3832.dat",  # Plate 2 x 10
        12: "2445.dat",  # Plate 2 x 12
    },
}


def get_plate_size(part_id):
    """
    Return (width, length) tuple for a plate part.
    Returns None if not found.
    """

    part = part_id.replace(".dat", "")

    for width, length_dict in PLATES.items():
        for length, ref in length_dict.items():
            if part == ref.replace(".dat", ""):
                return (width, length)

    return None


def build_plate(ctx, stud_x, stud_z, color, length):
    x = ctx.studs(stud_x)
    z = ctx.studs(stud_z)
    y = ctx.baseplate_top_origin_y
    part = PLATES[1][length]

    return f"1 {color} {x:.6f} {y:.6f} {z:.6f} 1 0 0 0 1 0 0 0 1 {part}"


def build_plate_rotated(ctx, stud_x, stud_z, color, length):
    x = ctx.studs(stud_x)
    z = ctx.studs(stud_z)
    y = ctx.baseplate_top_origin_y
    part = PLATES[1][length]

    # rotate 90° around Y
    return f"1 {color} {x:.6f} {y:.6f} {z:.6f} 0 0 1 0 1 0 -1 0 0 {part}"
