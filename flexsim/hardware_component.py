from __future__ import annotations
from typing import Dict, Optional

from flexsim.machine_op import MachineOp


class HardwareComponent:
    id_counter: int = 0
    id_map: Dict[int, HardwareComponent] = {}

    def __init__(self, name: str):
        HardwareComponent.id_counter += 1
        self.hardware_id = HardwareComponent.id_counter
        HardwareComponent.id_map[self.hardware_id] = self

        self.name = name

    @classmethod
    def get_component_by_id(cls, hw_id):
        return cls.id_map[hw_id]


    def get_machine_op_finish_time(self, machine_op: MachineOp, data_ready_time: int) -> int:
        """
        simulate one machine op finish time
        finish_time = max(hardware_ready_time, data_ready_time) + op_execution_time
        hardware_ready_time are maintained by class.
        :param data_ready_time: data ready
        :param machine_op: to be finished op
        :return:  finish time
        """
        return 0


class InterconnectComponent(HardwareComponent):
    """
    InterconnectComponent can only transfer data, can not execute any micro ops.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def register_compo(self, compo: GeneralComponent):
        pass

    def compute_transfer_latency(self):
        pass


class GeneralComponent(HardwareComponent):
    """
    GeneralComponent: do computing or storage or represent a module
    general component can only connect to interconnection component
    """

    def __init__(self, name: str, parent_compo: Optional[GeneralComponent, None] = None, ):
        super().__init__(name)

        self.parent_compo = parent_compo

        self.outer_comm_compo: Optional[InterconnectComponent] = None

    def connect_to(self, interconnection: InterconnectComponent):
        self.outer_comm_compo = interconnection
        interconnection.register_compo(self)
