from eth.vm.forks.berlin.computation import (
    BERLIN_PRECOMPILES
)
from eth.vm.forks.berlin.computation import (
    BerlinComputation,
)

from .opcodes import SEOUL_OPCODES

SEOUL_PRECOMPILES = BERLIN_PRECOMPILES


class SeoulComputation(BerlinComputation):
    """
    A class for all execution computations in the ``Berlin`` fork.
    """
    # Override
    opcodes = SEOUL_OPCODES
    _precompiles = SEOUL_PRECOMPILES