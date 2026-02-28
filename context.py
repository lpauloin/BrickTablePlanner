# context.py

from dataclasses import dataclass

STUD = 20
PLATE_HEIGHT = 8
BASEPLATE_THICKNESS = 8  # 1 plate


@dataclass
class SceneContext:
    """
    Defines the global coordinate system for the scene.
    """

    ground_y: float = 0.0  # Y coordinate of the TOP of the baseplate

    def studs(self, value: float) -> float:
        return value * STUD

    @property
    def baseplate_origin_y(self) -> float:
        """
        Returns the Y where the baseplate part origin must be placed
        so that its TOP is at ground_y.
        Baseplate origin is at its center.
        """
        return self.ground_y + BASEPLATE_THICKNESS / 2

    @property
    def baseplate_top_origin_y(self) -> float:
        """
        Returns the Y where the baseplate part origin must be placed
        so that its TOP is at ground_y.
        Baseplate origin is at its center.
        """
        return self.ground_y - BASEPLATE_THICKNESS / 2
