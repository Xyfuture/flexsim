from flexsim.hardware_base import BufferBase, GeneralBase


class SramBuffer(BufferBase):
    def __init__(self, name: str, parent_compo: GeneralBase):
        super().__init__(name, parent_compo)

    def get_read_latency(self, data_size: int):
        pass

    def get_write_latency(self, data_size: int):
        pass
