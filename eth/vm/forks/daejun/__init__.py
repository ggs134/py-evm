from typing import (
    Type,
)

from eth.rlp.blocks import BaseBlock
from eth.vm.forks.berlin import (
    BerlinVM,
)
from eth.vm.state import BaseState

from .blocks import DaejunBlock
from .headers import (
    compute_daejun_difficulty,
    configure_daejun_header,
    create_daejun_header_from_parent,
)
from .state import DaejunState


class DaejunVM(BerlinVM):
    # fork name
    fork = 'daejun'

    # classes
    block_class: Type[BaseBlock] = DaejunBlock
    _state_class: Type[BaseState] = DaejunState

    # Methods
    create_header_from_parent = staticmethod(create_daejun_header_from_parent)  # type: ignore
    compute_difficulty = staticmethod(compute_daejun_difficulty)    # type: ignore
    configure_header = configure_daejun_header