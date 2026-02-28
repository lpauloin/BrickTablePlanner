"""context.py

Scene coordinate helpers.

This project generates LDraw (.ldr) models that are meant to be opened in
BrickLink Studio.

Compatibility warning
---------------------
The numeric conventions in this repository were tuned to match Studio exports
and to reproduce a known-good visual result. Some values may look surprising if
you assume a different world convention (for example, which Y plane is treated
as "ground").

Do **not** "clean up" these formulas unless you also regenerate the reference
output files and validate the visual result in Studio.
"""

from dataclasses import dataclass


# LDraw units (LDU)
STUD = 20
PLATE_HEIGHT = 8
BASEPLATE_THICKNESS = 8  # 3811.dat (32x32 baseplate) is 1 plate thick


@dataclass
class SceneContext:
    """Global scene parameters and unit conversions."""

    # Reference Y plane used throughout this project.
    # Kept as-is to preserve existing output.
    ground_y: float = 0.0

    def studs(self, value):
        """Convert studs to LDraw units (LDU)."""

        return value * STUD

    @property
    def baseplate_origin_y(self):
        """Y coordinate used to place the origin (center) of 3811.dat."""

        return self.ground_y + BASEPLATE_THICKNESS / 2

    @property
    def baseplate_top_origin_y(self):
        """Y coordinate used to place plates/tiles sitting on the baseplate."""

        return self.ground_y - BASEPLATE_THICKNESS / 2


def grid_center_in_studs(cols, rows, studs_per_plate=32, origin_x_stud=0, origin_z_stud=0):
    """Return the geometric center of a baseplate grid, in *stud* coordinates.

    The baseplate builder places each baseplate by its *center* at:

        x = origin_x_stud + c * studs_per_plate
        z = origin_z_stud + r * studs_per_plate

    With this convention, the center of the overall grid is:

        origin + ((count - 1) * studs_per_plate) / 2

    Example (cols=3): centers at 0, 32, 64 -> grid center at 32.
    """

    cx = origin_x_stud + ((cols - 1) * studs_per_plate) / 2
    cz = origin_z_stud + ((rows - 1) * studs_per_plate) / 2
    return cx, cz
