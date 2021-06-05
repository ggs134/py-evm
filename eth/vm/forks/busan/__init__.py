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

    # using delegation tx
    using_delegation_tx = True

    # classes
    block_class: Type[BaseBlock] = BusanBlock
    _state_class: Type[BaseState] = BusanState

    # Methods
    create_header_from_parent = staticmethod(create_busan_header_from_parent)  # type: ignore
    compute_difficulty = staticmethod(compute_busan_difficulty)    # type: ignore
    configure_header = configure_busan_header

    #
    # Execution Delegation Transaction
    # This came from eth.vm.base.py -> VM.apply_transaction()
    #
    def apply_delegation_transaction(self,
                          header: BlockHeaderAPI,
                          transaction: SignedTransactionAPI
                          ) -> Tuple[ReceiptAPI, ComputationAPI]:
        self.validate_transaction_against_header(header, transaction)

        # Mark current state as un-revertable, since new transaction is starting...
        self.state.lock_changes()

        computation = self.state.apply_delegation_transaction(transaction)
        receipt = self.make_receipt(header, transaction, computation, self.state)
        self.validate_receipt(receipt)

        return receipt, computation