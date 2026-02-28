"""
minifig.py

Build a standard minifig from a Studio-exported LDraw template.
This avoids all origin/rotation pitfalls of minifig parts.

Workflow (one-time):
1) In BrickLink Studio, create ONE minifig made of parts:
   legs + torso + left arm + right arm + left hand + right hand + head
2) Export as LDraw (.ldr)
3) Copy the minifig lines into a file, e.g. "minifig.ldr"
   Keep ONLY the type-1 lines (starting with "1 "), remove baseplates, etc.
4) Use build_minifig(...) to place it anywhere, recolor parts, etc.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class LDrawType1:
    color: int
    x: float
    y: float
    z: float
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
    g: float
    h: float
    i: float
    part_id: str

    def to_line(self) -> str:
        return (
            f"1 {self.color} {self.x} {self.y} {self.z} "
            f"{self.a} {self.b} {self.c} {self.d} {self.e} {self.f} {self.g} {self.h} {self.i} "
            f"{self.part_id}"
        )

    @staticmethod
    def parse(line: str) -> "LDrawType1":
        parts = line.strip().split()
        if len(parts) < 15 or parts[0] != "1":
            raise ValueError(f"Not a type-1 line: {line!r}")

        color = int(parts[1])

        # coordinates as float
        x, y, z = map(float, parts[2:5])

        # matrix values as float
        a, b, c, d, e, f, g, h, i_ = map(float, parts[5:14])

        part_id = parts[14]

        return LDrawType1(color, x, y, z, a, b, c, d, e, f, g, h, i_, part_id)


def load_minifig_template(path: str | Path) -> List[LDrawType1]:
    """
    Load a template .ldr containing ONLY the minifig parts (type-1 lines).
    """
    path = Path(path)
    items: List[LDrawType1] = []
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
    parts = list(template)

    # --- centre X/Z uniquement ---
    cx = sum(p.x for p in parts) / len(parts)
    cz = sum(p.z for p in parts) / len(parts)

    # rotation validée (Y -90°)
    R = (0, 0, -1, 0, 1, 0, 1, 0, 0)

    dx = ctx.studs(stud_x)
    dz = ctx.studs(stud_z)

    transformed = []

    # 1️⃣ Transformation
    for p in parts:
        nx = p.x - cx
        ny = p.y
        nz = p.z - cz

        rx = R[0] * nx + R[1] * ny + R[2] * nz
        ry = R[3] * nx + R[4] * ny + R[5] * nz
        rz = R[6] * nx + R[7] * ny + R[8] * nz

        transformed.append((p, rx, ry, rz))

    # 🔥 CORRECTION VERTICALE RÉELLE
    # Les pieds (3816/3817) doivent être à Y = -30
    # dy = ctx.ground_y - 30
    dy = ctx.baseplate_origin_y - 30

    out = []

    # 2️⃣ Reconstruction finale
    for p, rx, ry, rz in transformed:

        final_x = rx + dx
        final_y = ry + dy
        final_z = rz + dz

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
            f"1 {p.color} "
            f"{final_x} {final_y} {final_z} "
            f"{a} {b} {c} {d} {e} {f} {g} {h} {i_} "
            f"{p.part_id}"
        )

    return out
