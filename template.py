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


def load_template(path):
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


def normalize_template_inplace(parts, epsilon=1e-5):
    """
    Normalize a Studio-exported LDraw template in place.

    This function modifies the given part objects directly.

    It:
    - Recenters the model around (0,0) in X/Z
    - Rounds coordinates to integer LDU
    - Cleans floating-point noise in rotation matrices
    - Preserves real rotations (arms, head tilt, etc.)

    Parameters
    ----------
    parts : iterable
        Iterable of part objects (with x, y, z, a..i attributes)
    epsilon : float
        Threshold used to clean near-zero / near-one matrix values
    """

    parts = list(parts)

    if not parts:
        return

    # --- 1️⃣ Compute geometric center in X/Z ---
    cx = sum(p.x for p in parts) / len(parts)
    cz = sum(p.z for p in parts) / len(parts)

    # --- 2️⃣ Apply normalization ---
    for p in parts:

        # Recenter (X/Z only)
        p.x = round(p.x - cx)
        p.y = round(p.y)
        p.z = round(p.z - cz)

        # Matrix cleanup helper
        def clean(v):
            if abs(v) < epsilon:
                return 0
            if abs(v - 1) < epsilon:
                return 1
            if abs(v + 1) < epsilon:
                return -1
            return v

        # Clean orientation matrix
        p.a = clean(p.a)
        p.b = clean(p.b)
        p.c = clean(p.c)
        p.d = clean(p.d)
        p.e = clean(p.e)
        p.f = clean(p.f)
        p.g = clean(p.g)
        p.h = clean(p.h)
        p.i = clean(p.i)
