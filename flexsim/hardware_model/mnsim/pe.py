from typing import Optional, Dict

from flexsim.hardware_base import GeneralBase, HardwareConfig
from flexsim.micro_graph.micro_op import Operation


class PEConfig(HardwareConfig):
    adc_num: int = 0

    def __init__(self, config_dict: Optional[Dict] = None):
        super().__init__(config_dict)


class PE(GeneralBase):
    def __init__(self, name: str, parent_compo: Optional[GeneralBase] = None):
        super().__init__(name, parent_compo)

    def execute(self, operation: Operation):
        pass