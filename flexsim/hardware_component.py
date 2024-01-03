from __future__ import annotations
from typing import Dict


class HardwareComponent:
    id_counter: int = 0
    id_map:Dict[int,HardwareComponent] = {}

    def __init__(self):
        HardwareComponent.id_counter += 1
        self.hardware_id = HardwareComponent.id_counter
        HardwareComponent.id_map[self.hardware_id] = self

    @classmethod
    def get_component_by_id(cls,id):
        return cls.id_map[id]

