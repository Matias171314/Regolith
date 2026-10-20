"""Shared inventory data: the first five slots are the quick-access bar."""

from dataclasses import dataclass


@dataclass
class ItemStack:
    """A module type and the number of units stored together."""

    module_class: type
    quantity: int

    def preview(self):
        return self.module_class(0, 0)


class Inventory:
    """Stores item stacks shared by the backpack and quick-access bar."""

    def __init__(self):
        self.slots = [None] * 15

    def add(self, module_class, quantity=1):
        if quantity <= 0:
            return False
        for stack in self.slots:
            if stack is not None and stack.module_class is module_class:
                stack.quantity += quantity
                return True
        for index, stack in enumerate(self.slots):
            if stack is None:
                self.slots[index] = ItemStack(module_class, quantity)
                return True
        return False

    def consume(self, index):
        stack = self.slots[index]
        if stack is None:
            return False
        stack.quantity -= 1
        if stack.quantity == 0:
            self.slots[index] = None
        return True
