from eth.vm.forks.berlin.state import (
    BerlinState
)

from .computation import DaejunComputation


class DaejunState(BerlinState):
    computation_class = DaejunComputation
