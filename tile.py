TILES = {
    1: {
        1: "3070b.dat",  # Tile 1x1
        2: "3069b.dat",  # Tile 1x2
        3: "63864.dat",  # Tile 1x3
        4: "2431b.dat",  # Tile 1x4
        6: "6636.dat",  # Tile 1x6
        8: "4162.dat",  # Tile 1x8
    },
    2: {
        2: "3068b.dat",  # Tile 2x2
        3: "26603.dat",  # Tile 2x3
        4: "87079.dat",  # Tile 2x4
        6: "69729.dat",  # Tile 2x6
    },
}


def get_tile_size(part_id):
    part = part_id.replace(".dat", "")

    for width, length_dict in TILES.items():
        for length, ref in length_dict.items():
            if part == ref.replace(".dat", ""):
                return (width, length)

    return None
