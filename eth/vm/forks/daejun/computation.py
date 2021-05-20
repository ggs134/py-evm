from eth.vm.forks.berlin.computation import (
    BERLIN_PRECOMPILES
)
from eth.vm.forks.berlin.computation import (
    BerlinComputation,
)

from .opcodes import DAEJUN_OPCODES

DAEJUN_PRECOMPILES = BERLIN_PRECOMPILES


class DaejunComputation(BerlinComputation):
    """
    A class for all execution computations in the ``Berlin`` fork.
    """
    # Override
    opcodes = DAEJUN_OPCODES
    _precompiles = DAEJUN_PRECOMPILES