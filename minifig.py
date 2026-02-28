"""minifig.py

Load a BrickLink Studio-exported minifig template (type-1 LDraw lines) and
reposition it on a target stud coordinate.

The key idea is simple:
  1) Take the exported template as-is (no manual editing besides keeping only
     type-1 lines).
  2) Recentre the template in X/Z around its own centroid.
  3) Apply a fixed rotation (Studio template facing) and translate to the
     desired stud coordinate.

This module keeps behavior compatible with the current project output.
"""

from pathlib import Path


class LDrawType1:
    """Minimal representation of an LDraw type-1 line."""

    def __init__(self, color, x, y, z, a, b, c, d, e, f, g, h, i, part_id):
        self.color = int(color)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)
        self.e = float(e)
        self.f = float(f)
        self.g = float(g)
        self.h = float(h)
        self.i = float(i)
        self.part_id = str(part_id)

    def to_line(self):
        return (
            f"1 {self.color} {self.x} {self.y} {self.z} "
            f"{self.a} {self.b} {self.c} {self.d} {self.e} {self.f} {self.g} {self.h} {self.i} "
            f"{self.part_id}"
        )

    @staticmethod
    def parse(line):
        parts = line.strip().split()
        if len(parts) < 15 or parts[0] != "1":
            raise ValueError(f"Not a type-1 line: {line!r}")

        return LDrawType1(
            parts[1],
            parts[2],
            parts[3],
            parts[4],
            parts[5],
            parts[6],
            parts[7],
            parts[8],
            parts[9],
            parts[10],
            parts[11],
            parts[12],
            parts[13],
            parts[14],
        )


def load_minifig_template(path):
    """Load a template .ldr file containing ONLY the minifig type-1 lines."""

    path = Path(path)
    items = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("0"):
            continue
        if raw.startswith("1 "):
            items.append(LDrawType1.parse(raw))

    if not items:
        raise ValueError(f"No type-1 lines found in template: {path}")
    return items


def build_minifig(ctx, template, stud_x, stud_z):
    """
    Reposition a minifig template to (stud_x, stud_z) in stud space.

    The template orientation is preserved exactly as exported.
    No rotation is applied.
    """

    parts = list(template)

    # Compute template center in X/Z (we do not touch Y)
    cx = sum(p.x for p in parts) / len(parts)
    cz = sum(p.z for p in parts) / len(parts)

    # Target position in LDraw units
    dx = ctx.studs(stud_x)
    dz = ctx.studs(stud_z)
    dy = ctx.baseplate_origin_y

    out = []

    for p in parts:

        # Recenter around template origin
        nx = p.x - cx
        ny = p.y
        nz = p.z - cz

        # Translate to final position
        final_x = nx + dx
        final_y = ny + dy
        final_z = nz + dz

        # IMPORTANT: keep original orientation matrix
        out.append(
            f"1 {p.color} {final_x} {final_y} {final_z} "
            f"{p.a} {p.b} {p.c} {p.d} {p.e} {p.f} {p.g} {p.h} {p.i} "
            f"{p.part_id}"
        )

    return out
