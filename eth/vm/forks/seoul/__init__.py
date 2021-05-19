from typing import (
    Type,
)

from eth.rlp.blocks import BaseBlock
from eth.vm.forks.berlin import (
    BerlinVM,
)
from eth.vm.state import BaseState

from .blocks import SeoulBlock
from .headers import (
    compute_seoul_difficulty,
    configure_seoul_header,
    create_seoul_header_from_parent,
)
from .state import SeoulState


class SeoulVM(BerlinVM):
    # fork name
    fork = 'seoul'

    # classes
    block_class: Type[BaseBlock] = SeoulBlock
    _state_class: Type[BaseState] = SeoulState

    # Methods
    create_header_from_parent = staticmethod(create_seoul_header_from_parent)  # type: ignore
    compute_difficulty = staticmethod(compute_seoul_difficulty)    # type: ignore
    configure_header = configure_seoul_header