from eth.vm.forks.berlin.computation import (
    BERLIN_PRECOMPILES
)
from eth.vm.forks.berlin.computation import (
    BerlinComputation,
)

from .opcodes import BUSAN_OPCODES

BUSAN_PRECOMPILES = BERLIN_PRECOMPILES


class BusanComputation(BerlinComputation):
    """
    A class for all execution computations in the ``Berlin`` fork.
    """
    # Override
    opcodes = BUSAN_OPCODES
    _precompiles = BUSAN_PRECOMPILES