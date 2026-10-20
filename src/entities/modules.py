"""Buildings available for the first version of the lunar base.

Descriptions express their intended roles. Buildings can be inspected and
recovered; resource processing will be implemented with each mechanic.
"""

from entities.base_entity import BaseEntity


class Module(BaseEntity):
    """Base building with a description of its purpose."""

    def __init__(self, grid_x, grid_y, color, name, description):
        super().__init__(grid_x, grid_y, color, name)
        self.description = description


class SolarPanel(Module):
    """Provides electricity for the base."""

    def __init__(self, grid_x, grid_y):
        super().__init__(
            grid_x,
            grid_y,
            (230, 167, 30),
            "Solar Panel",
            "Produces electricity from sunlight.",
        )
        self.power_output = 15


class OxygenGenerator(Module):
    """Uses water and electricity to supply oxygen."""

    def __init__(self, grid_x, grid_y):
        super().__init__(
            grid_x,
            grid_y,
            (178, 219, 235),
            "Oxygen Generator",
            "Uses water and electricity to produce oxygen for the base and suit.",
        )
        self.oxygen_output = 15


class Habitat(Module):
    """Provides shelter and a place to rest."""

    def __init__(self, grid_x, grid_y):
        super().__init__(
            grid_x,
            grid_y,
            (200, 180, 220),
            "Habitat",
            "Provides shelter and a place to sleep, using electricity and oxygen.",
        )


class WaterTank(Module):
    """Stores water for the base's facilities."""

    def __init__(self, grid_x, grid_y):
        super().__init__(
            grid_x,
            grid_y,
            (60, 130, 210),
            "Water Tank",
            "Stores water for crops and oxygen production.",
        )


class Greenhouse(Module):
    """Provides space to plant and care for food crops."""

    def __init__(self, grid_x, grid_y):
        super().__init__(
            grid_x,
            grid_y,
            (90, 180, 100),
            "Greenhouse",
            "Provides space to grow food, using water and electricity.",
        )
