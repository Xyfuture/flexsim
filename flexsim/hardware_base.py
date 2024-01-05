from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Optional, Union, List, overload

from flexsim.machine_op import MachineOp


class HardwareBase:
    id_counter: int = 0
    id_map: Dict[int, HardwareBase] = {}

    def __init__(self, name: str, parent_compo: Optional[HardwareBase] = None):
        HardwareBase.id_counter += 1
        self.hardware_id = HardwareBase.id_counter
        HardwareBase.id_map[self.hardware_id] = self

        self.name = name
        self.parent_compo = parent_compo

    @classmethod
    def get_component_by_id(cls, id):
        return cls.id_map[id]

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

    def __hash__(self):
        return self.hardware_id

    def __eq__(self, other):
        assert isinstance(other, HardwareBase)
        return self.hardware_id == other.hardware_id


class BufferBase(HardwareBase):
    def __init__(self, name: str, parent_compo: Optional[GeneralBase] = None, as_gateway: bool = True):
        super().__init__(name, parent_compo)

        self._as_gateway: bool = as_gateway

    @property
    def as_gateway(self):
        return self._as_gateway

    def get_read_latency(self, data_size: int):
        pass

    def get_write_latency(self, data_size: int):
        pass


class InterconnectBase(HardwareBase):
    """
    InterconnectComponent can only transfer data, can not execute any micro ops.
    """

    def __init__(self, name: str, parent_compo: Optional[GeneralBase] = None):
        super().__init__(name, parent_compo)
        self.connected_components = []
        self.gateway_components = []

    def register_compo(self, compo: Union[GeneralBase, BufferBase]):
        self.connected_components.append(compo)
        if isinstance(compo, BufferBase) and compo.as_gateway:
            self.gateway_components.append(compo)

    def compute_transfer_latency(self, data_size: int, start_time: int):
        pass


class GeneralBase(HardwareBase):
    """
    GeneralComponent: do computing or storage or represent a module
    general component can only connect to interconnection component
    """

    def __init__(self, name: str, parent_compo: Optional[GeneralBase] = None, ):
        super().__init__(name, parent_compo)

        self.interconnections: List[InterconnectBase] = []

        self.cached_path: Dict[HardwareBase, DataTransferPath] = {}

    def connect_to(self, interconnection: InterconnectBase):
        interconnection.register_compo(self)
        self.interconnections.append(interconnection)

    def find_path_to(self, dst: HardwareBase) -> DataTransferPath:
        # just find a way to there
        # not guarantee for the best path
        # use bfs to find the way

        visited_network: Dict[InterconnectBase, None] = {}
        pre_path:Dict[InterconnectBase,DataTransferPathNode] = {}
        pending_queue = deque()



        pass

    def find_path_from(self, src: HardwareBase) -> DataTransferPath:
        reversed_path = self.find_path_to(src)
        new_path = reversed_path.get_reversed_path()
        return new_path


@dataclass
class DataTransferPathNode:
    src: HardwareBase
    dst: HardwareBase
    interconnection: InterconnectBase


class DataTransferPath:
    def __init__(self, path_src: HardwareBase, path_dst: HardwareBase):
        self.path_src = path_src
        self.path_dst = path_dst

        self.node_list: List[DataTransferPathNode] = []

    def append(self, src: HardwareBase, dst: HardwareBase, network: InterconnectBase):
        next_node = DataTransferPathNode(src, dst, network)
        self.append_node(next_node)

    def append_node(self, next_node: DataTransferPathNode):
        if self.node_list:
            last_node = self.node_list[-1]
            assert last_node.dst == next_node.src

        self.node_list.append(next_node)

    def check_path(self) -> bool:
        pass

    def compute_transfer_latency(self, data_size: int, start_time: int) -> int:
        """
        :param data_size: unit Byte
        :param start_time:
        :return: total transfer latency
        """
        assert self.node_list[0].src == self.path_src and self.node_list[-1].dst == self.path_dst, "Wrong Path"

        transfer_latency = 0

        for node in self.node_list:
            tmp_src, tmp_dst, network = node.src, node.dst, node.interconnection

            if isinstance(tmp_src, BufferBase):
                transfer_latency += tmp_src.get_read_latency(data_size)

            transfer_latency += network.compute_transfer_latency(data_size, start_time)

            if isinstance(tmp_dst, BufferBase):
                transfer_latency += tmp_dst.get_write_latency(data_size)

        return transfer_latency

    def get_reversed_path(self) -> DataTransferPath:
        reversed_path = DataTransferPath(self.path_dst, self.path_src)

        for node in self.node_list[::, -1]:
            reversed_path.append(node.dst, node.src, node.interconnection)

        return reversed_path
