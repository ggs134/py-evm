from typing import (
    Type,
)

from eth.rlp.blocks import BaseBlock
from eth.vm.forks.berlin import (
    BerlinVM,
)
from eth.vm.state import BaseState

from .blocks import BusanBlock
from .headers import (
    compute_busan_difficulty,
    configure_busan_header,
    create_busan_header_from_parent,
)
from .state import BusanState


class BusanVM(BerlinVM):
    # fork name
    fork = 'busan'

    # classes
    block_class: Type[BaseBlock] = BusanBlock
    _state_class: Type[BaseState] = BusanState

    # Methods
    create_header_from_parent = staticmethod(create_busan_header_from_parent)  # type: ignore
    compute_difficulty = staticmethod(compute_busan_difficulty)    # type: ignore
    configure_header = configure_busan_header