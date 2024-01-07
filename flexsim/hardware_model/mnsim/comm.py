from typing import Optional, List, Tuple

from flexsim.hardware_base import HardwareBase, InterconnectBase, GeneralBase, DataTransferPathNode, NetworkCompoPair


class MeshNoC(InterconnectBase):
    def __init__(self, name, parent_compo: Optional[GeneralBase] = None, ):
        super().__init__(name, parent_compo, )

    def compute_transfer_latency(self, data_size: int, start_time: int):
        pass

    def get_adj_networks(self, entry_compo: GeneralBase) -> List[NetworkCompoPair]:
        network_compo_pair_list = []
        for compo in self.connected_components:
            if hasattr(compo, 'as_gateway') and compo.as_gateway:
                for network in compo.interconnections:
                    if network is not self:
                        network_compo_pair_list.append(NetworkCompoPair(network, compo))

        return network_compo_pair_list

    def find_path_to(self, src: GeneralBase, dst: GeneralBase) -> Optional[DataTransferPathNode]:
        # src must in the network, dst may not
        assert src in self.connected_components
        if dst in self.connected_components:
            return DataTransferPathNode(src, dst, self)
        return None


class HTreeBus(InterconnectBase):
    def __init__(self, name: str, parent_compo: Optional[GeneralBase] = None):
        super().__init__(name, parent_compo)
        self.root_compo: Optional[GeneralBase] = None
        self.leaf_compos: List[GeneralBase] = []

    def compute_transfer_latency(self, data_size: int, start_time: int):
        pass

    def get_adj_networks(self, entry_compo: GeneralBase) -> List[NetworkCompoPair]:
        network_pair_list = []
        if entry_compo is self.root_compo:
            for leaf_compo in self.leaf_compos:
                if hasattr(leaf_compo, 'as_gateway') and leaf_compo.as_gateway:
                    for network in leaf_compo.interconnections:
                        if network is not self:
                            network_pair_list.append(NetworkCompoPair(network, leaf_compo))

        elif entry_compo in self.leaf_compos:
            if hasattr(self.root_compo, 'as_gateway') and self.root_compo.as_gateway:
                for network in self.root_compo.interconnections:
                    if network is not self:
                        network_pair_list.append(NetworkCompoPair(network,self.root_compo))

        return network_pair_list

    def find_path_to(self, src: GeneralBase, dst: GeneralBase) -> Optional[DataTransferPathNode]:
        assert src in self.connected_components

        if src is self.root_compo:
            if dst in self.leaf_compos:
                return DataTransferPathNode(src,dst,self)
        elif src in self.leaf_compos:
            if dst is self.root_compo:
                return DataTransferPathNode(src,dst,self)
        return None

