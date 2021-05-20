from rlp.sedes import (
    CountableList,
)
from eth.rlp.headers import (
    BlockHeader,
)
from eth.vm.forks.berlin.blocks import (
    BerlinBlock,
)

from .transactions import (
    DaejunTransactionBuilder,
)


class DaejunBlock(BerlinBlock):
    transaction_builder = DaejunTransactionBuilder
    fields = [
        ('header', BlockHeader),
        ('transactions', CountableList(transaction_builder)),
        ('uncles', CountableList(BlockHeader))
    ]
