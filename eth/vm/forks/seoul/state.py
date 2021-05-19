from eth.vm.forks.berlin.state import (
    BerlinState
)

from .computation import SeoulComputation


class SeoulState(BerlinState):
    computation_class = SeoulComputation
