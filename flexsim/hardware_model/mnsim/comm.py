from typing import Optional, List, Tuple

from flexsim.hardware_base import HardwareBase, InterconnectBase, GeneralBase, DataTransferPathNode


class MeshNoC(InterconnectBase):
    def __init__(self, name, parent_compo: Optional[GeneralBase] = None, ):
        super().__init__(name, parent_compo, )




    def compute_transfer_latency(self, data_size: int, start_time: int):
        pass

    def get_adj_networks(self, entry_compo) -> List[Tuple[HardwareBase, InterconnectBase]]:
        for compo in self.connected_components:
            if hasattr(compo,'as_gateway') and compo.as_gateway:
                for network in compo.
        pass

    def find_path_to(self, src, dst) -> Optional[DataTransferPathNode]:
        pass


class HTreeBus(InterconnectBase):
    def __init__(self):
        pass
