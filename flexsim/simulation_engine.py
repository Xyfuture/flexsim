from collections import deque
from typing import List, Dict, Deque

from flexsim._node import Node
from flexsim.hardware_base import HardwareBase
from flexsim.micro_graph.micro_graph import MicroGraph
from flexsim.micro_graph.micro_op import MicroOpNode
from flexsim.micro_graph.micro_tensor import MicroTensorNode


class SimpleSimulationEngine:
    def __init__(self):
        self.micro_graph: MicroGraph = None
        self.hardware_system: HardwareBase = None

        self.simulation_time: float = 0  # unit:ns

    def run_simulation(self) -> int:
        # reset all settings
        self.simulation_time = 0
        micro_op_node_topo_list = self.toposort()

        for micro_op_node in micro_op_node_topo_list:
            micro_op = micro_op_node.micro_op

            for operation in micro_op.operation_list:
                micro_op.component.execute(operation)

        sim_max_time = 0
        # get final time
        for node in self.micro_graph.nodes:
            if isinstance(node, MicroTensorNode):
                micro_tensor = node.micro_tensor
                if micro_tensor.get_max_time() > sim_max_time:
                    sim_max_time = micro_tensor.get_max_time()
        self.simulation_time = sim_max_time
        return sim_max_time

    def toposort(self) -> List[MicroOpNode]:
        topo_order_list: List[Node] = []

        input_dep_num: Dict[Node, int] = {}
        pending_queue: Deque[Node] = deque()

        for node in self.micro_graph.nodes:
            input_dep_num[node] = len(node.all_input_nodes)
            if len(node.all_input_nodes) == 0:
                pending_queue.append(node)

        while len(pending_queue):
            cur_node = pending_queue.popleft()
            topo_order_list.append(cur_node)
            for node in cur_node.all_output_nodes:
                input_dep_num[node] -= 1
                if input_dep_num[node] == 0:
                    pending_queue.append(node)

        micro_op_topo_list: List[MicroOpNode] = []
        for node in topo_order_list:
            if isinstance(node, MicroOpNode):
                micro_op_topo_list.append(node)

        return micro_op_topo_list
