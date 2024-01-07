from flexsim.hardware_base import BufferBase, HardwareBase, GeneralBase


class SramBuffer(BufferBase):
    def __init__(self, name: str, parent_compo: GeneralBase):
        super().__init__(name, parent_compo)
