from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Optional, Union, List, overload, Tuple

from typing_extensions import Deque

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
        self.connected_components: Dict[HardwareBase, None] = {}
        self.gateway_components: Dict[HardwareBase, None] = {}

    def register_compo(self, compo: Union[GeneralBase, BufferBase]):
        self.connected_components.setdefault(compo)
        if isinstance(compo, BufferBase) and compo.as_gateway:
            self.gateway_components.setdefault(compo)

    def compute_transfer_latency(self, data_size: int, start_time: int):
        pass

    def get_adj_networks(self, entry_compo) -> List[Tuple[HardwareBase, InterconnectBase]]:
        """
        BFS find adj nodes
        :param entry_compo: from this compo into the network
        :return: other adjacency networks can be accessed by entry compo
        """
        pass

    def find_path_to(self, src, dst) -> Optional[DataTransferPathNode]:
        """
        src and dst should in this network
        if there is a path from src to dst,
        return DataTransferPathNode(src,dst,self)
        :param src:
        :param dst:
        :return:
        """
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

        transfer_path = DataTransferPath(self, dst)

        # first check whether dst and src in the same network (just src network)
        for network in self.interconnections:
            path_to_dst = network.find_path_to(self, dst)
            if path_to_dst:
                transfer_path.append_node(path_to_dst)
                return transfer_path

        # network_combo: containing an entry compo(in the network) and the network
        NetworkComboType = Tuple[HardwareBase, InterconnectBase]
        visited_network_combo: Dict[NetworkComboType, None] = {}
        pre_path: Dict[NetworkComboType, NetworkComboType] = {}
        pending_queue: Deque[NetworkComboType] = deque()

        # push current network adj to queue
        for network in self.interconnections:
            adj_network_combo_list = network.get_adj_networks(self)
            for adj_network_combo in adj_network_combo_list:
                pending_queue.append(adj_network_combo)
                visited_network_combo.setdefault(adj_network_combo)
                pre_path[adj_network_combo] = (self, network)

        while len(pending_queue):
            current_network_combo = pending_queue.pop()
            current_network = current_network_combo[1]
            current_entry_compo = current_network_combo[0]
            path_to_dst = current_network.find_path_to(current_entry_compo, dst)

            if path_to_dst:
                # find way out
                # build the path recursively from pre_path
                transfer_path.prepend_node(path_to_dst)

                tmp_combo = current_network_combo
                while tmp_combo[0] is not self:
                    pre_combo = pre_path[tmp_combo]

                    transfer_path.perpend(pre_combo[0], tmp_combo[0], pre_combo[1])

                    tmp_combo = pre_combo

                return transfer_path

            adj_network_combo_list = current_network.get_adj_networks(current_entry_compo)
            for adj_network_combo in adj_network_combo_list:
                if adj_network_combo not in visited_network_combo:
                    pending_queue.append(adj_network_combo)
                    visited_network_combo.setdefault(adj_network_combo)

                    # set previous path
                    pre_path[adj_network_combo] = current_network_combo

        pass

    def find_path_from(self, src: GeneralBase) -> DataTransferPath:
        return src.find_path_to(self)


@dataclass
class DataTransferPathNode:
    src: HardwareBase
    dst: HardwareBase
    interconnection: InterconnectBase


class DataTransferPath:
    def __init__(self, path_src: HardwareBase, path_dst: HardwareBase):
        self.path_src = path_src
        self.path_dst = path_dst

        self.node_queue: Deque[DataTransferPathNode] = deque()

    def append(self, src: HardwareBase, dst: HardwareBase, network: InterconnectBase):
        # order : from src to dst
        next_node = DataTransferPathNode(src, dst, network)
        self.append_node(next_node)

    def append_node(self, next_node: DataTransferPathNode):
        # order : from src to dst
        if len(self.node_queue):
            # check
            last_node = self.node_queue[-1]
            assert last_node.dst == next_node.src

        self.node_queue.append(next_node)

    def perpend(self, src: HardwareBase, dst: HardwareBase, network: InterconnectBase):
        # order: from dst to src (reversed)
        pre_node = DataTransferPathNode(src, dst, network)
        self.prepend_node(pre_node)

    def prepend_node(self, pre_node: DataTransferPathNode):
        # order: from dst to src (reversed)
        if len(self.node_queue):
            first_node = self.node_queue[0]
            assert first_node.src == pre_node.dst

        self.node_queue.appendleft(pre_node)

    def check_path(self) -> bool:
        pass

    def compute_transfer_latency(self, data_size: int, start_time: int) -> int:
        """
        :param data_size: unit Byte
        :param start_time:
        :return: total transfer latency
        """
        assert self.node_queue[0].src == self.path_src and self.node_queue[-1].dst == self.path_dst, "Wrong Path"

        transfer_latency = 0

        for node in self.node_queue:
            tmp_src, tmp_dst, network = node.src, node.dst, node.interconnection

            if isinstance(tmp_src, BufferBase):
                transfer_latency += tmp_src.get_read_latency(data_size)

            transfer_latency += network.compute_transfer_latency(data_size, start_time)

            if isinstance(tmp_dst, BufferBase):
                transfer_latency += tmp_dst.get_write_latency(data_size)

        return transfer_latency

    def get_reversed_path(self) -> DataTransferPath:
        reversed_path = DataTransferPath(self.path_dst, self.path_src)

        for node in self.node_queue[::, -1]:
            reversed_path.append(node.dst, node.src, node.interconnection)

        return reversed_path
