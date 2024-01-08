from typing import Optional, Tuple

from flexsim.hardware_base import GeneralBase, HardwareConfig
from flexsim.machine_op import MachineOp
from flexsim.micro_graph.micro_op import Operation


class OP_MatrixVectorMul(MachineOp):
    def __init__(self):
        super().__init__()


class XbarUnitConfig(HardwareConfig):
    xbar_size: Tuple[int, int] = (128, 128)
    xbar_latency: float = 30  # unit: ns
    xbar_cell_precision: int = 8

    dac_resolution: int = 1  # unit: bit
    dac_latency: float = 1  # unit: ns
    dac_count: int = 128  # per xbar

    adc_resolution: int = 8  # unit: bit
    adc_latency: float = 1  # unit: ns
    adc_count: int = 2  # per xbar

    sample_hold_latency: float = 1

    shift_adder_latency: float = 1

    input_buffer_latency: float = 1

    output_buffer_latency: float = 1

    def __init__(self, config_dict: Optional[dict] = None):
        super().__init__(config_dict)


class XbarUnit(GeneralBase):
    def __init__(self, name: str, parent_compo: Optional[GeneralBase] = None,
                 xbar_config: Optional[XbarUnitConfig] = None):
        super().__init__(name, parent_compo)

        self.config = xbar_config

    def execute(self, operation: Operation):
        machine_op = operation.machine_op
        if isinstance(machine_op, OP_MatrixVectorMul):
            pass

    def compute_machine_op_latency(self, machine_op: MachineOp):
        pass
