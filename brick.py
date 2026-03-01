BRICKS = {
    1: {
        1: "3005.dat",  # Brick 1x1
        2: "3004.dat",  # Brick 1x2
        3: "3622.dat",  # Brick 1x3
        4: "3010.dat",  # Brick 1x4
        6: "3009.dat",  # Brick 1x6
        8: "3008.dat",  # Brick 1x8
    },
    2: {
        2: "3003.dat",  # Brick 2x2
        3: "3002.dat",  # Brick 2x3
        4: "3001.dat",  # Brick 2x4
        6: "2456.dat",  # Brick 2x6
        8: "3007.dat",  # Brick 2x8
    },
}


def get_brick_size(part_id):
    """
    Return (width, length) tuple for a brick part.
    Returns None if not found.
    """

    part = part_id.replace(".dat", "")

    for width, length_dict in BRICKS.items():
        for length, ref in length_dict.items():
            if part == ref.replace(".dat", ""):
                return (width, length)

    return None
