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
    """Reposition a minifig template to (stud_x, stud_z) in studs."""

    parts = list(template)

    # Center in X/Z only (we keep Y as provided by the template)
    cx = sum(p.x for p in parts) / len(parts)
    cz = sum(p.z for p in parts) / len(parts)

    # Rotation validated for the Studio-exported template:
    # rotate around Y by -90 degrees.
    R = (
        0, 0, -1,
        0, 1, 0,
        1, 0, 0,
    )

    dx = ctx.studs(stud_x)
    dz = ctx.studs(stud_z)

    transformed = []
    for p in parts:
        nx = p.x - cx
        ny = p.y
        nz = p.z - cz

        rx = R[0] * nx + R[1] * ny + R[2] * nz
        ry = R[3] * nx + R[4] * ny + R[5] * nz
        rz = R[6] * nx + R[7] * ny + R[8] * nz
        transformed.append((p, rx, ry, rz))

    # Vertical alignment: keep current output behavior.
    # In our reference template, the feet should end up on Y = -30.
    dy = ctx.baseplate_origin_y - 30

    out = []
    for p, rx, ry, rz in transformed:
        final_x = rx + dx
        final_y = ry + dy
        final_z = rz + dz

        # Rotate the part orientation matrix as well.
        a = R[0] * p.a + R[1] * p.d + R[2] * p.g
        b = R[0] * p.b + R[1] * p.e + R[2] * p.h
        c = R[0] * p.c + R[1] * p.f + R[2] * p.i
        d = R[3] * p.a + R[4] * p.d + R[5] * p.g
        e = R[3] * p.b + R[4] * p.e + R[5] * p.h
        f = R[3] * p.c + R[4] * p.f + R[5] * p.i
        g = R[6] * p.a + R[7] * p.d + R[8] * p.g
        h = R[6] * p.b + R[7] * p.e + R[8] * p.h
        i_ = R[6] * p.c + R[7] * p.f + R[8] * p.i

        out.append(
            f"1 {p.color} {final_x} {final_y} {final_z} "
            f"{a} {b} {c} {d} {e} {f} {g} {h} {i_} "
            f"{p.part_id}"
        )

    return out
