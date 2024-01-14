from typing import Optional, Tuple

from flexsim.hardware_base import GeneralBase, HardwareConfig
from flexsim.machine_op import MachineOp
from flexsim.micro_graph.micro_op import Operation
import math


class OP_MatrixVectorMul(MachineOp):
    def __init__(self, input_precision: int, weight_precision: int):
        super().__init__()
        self.input_precision = input_precision
        self.weight_precision = weight_precision


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

        self.unit_ready_time: float = 0

    def execute(self, operation: Operation):
        machine_op = operation.machine_op
        if isinstance(machine_op, OP_MatrixVectorMul):
            pass

    def compute_machine_op_latency(self, machine_op: MachineOp) -> float:
        if isinstance(machine_op, OP_MatrixVectorMul):
            # matrix vector mul
            # default pipeline mdoe

            input_times = math.ceil(machine_op.input_precision / self.config.dac_resolution)

            dac_times = math.ceil(self.config.xbar_size[0] / self.config.dac_count)
            adc_times = math.ceil(self.config.xbar_size[1] / self.config.adc_count)

            single_front_stage_latency = self.config.input_buffer_latency + \
                                         self.config.dac_latency + \
                                         self.config.xbar_latency + \
                                         self.config.sample_hold_latency

            back_stage_pipe_latency = max(self.config.adc_latency,
                                          self.config.shift_adder_latency + self.config.output_buffer_latency)
            single_back_stage_latency = self.config.adc_latency + self.config.shift_adder_latency + self.config.output_buffer_latency + \
                                        (adc_times - 1) * back_stage_pipe_latency

            full_stage_pipe_latency = max(single_front_stage_latency, single_back_stage_latency)
            total_latency = single_back_stage_latency + single_back_stage_latency + \
                            (input_times * dac_times - 1) * full_stage_pipe_latency
            return total_latency
