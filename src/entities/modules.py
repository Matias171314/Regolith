from entities.base_entity import BaseEntity

class SolarPanel(BaseEntity):
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, (230, 167, 30), "Solar Panel")
        self.power_output = 15

    def update(self):
        print(f"{self.name} generating {self.power_output} kW of energy.")

class OxygenGenerator(BaseEntity):
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, (178, 219, 235), "Oxygen Generator")
        self.oxygen_output = 15
