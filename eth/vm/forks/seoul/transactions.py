from eth_keys.datatypes import PrivateKey
from eth_typing import Address

from eth._utils.transactions import (
    create_transaction_signature,
)

from eth.vm.forks.berlin.transactions import (
    BerlinLegacyTransaction,
    BerlinUnsignedLegacyTransaction,
    BerlinTransactionBuilder,
)


class SeoulLegacyTransaction(BerlinLegacyTransaction):
    pass


class SeoulUnsignedLegacyTransaction(BerlinUnsignedLegacyTransaction):
    def as_signed_transaction(self,
                              private_key: PrivateKey,
                              chain_id: int = None) -> BerlinLegacyTransaction:
        v, r, s = create_transaction_signature(self, private_key, chain_id=chain_id)
        return BerlinLegacyTransaction(
            nonce=self.nonce,
            gas_price=self.gas_price,
            gas=self.gas,
            to=self.to,
            value=self.value,
            data=self.data,
            v=v,
            r=r,
            s=s,
        )


class SeoulTransactionBuilder(BerlinTransactionBuilder):
    # Override
    legacy_signed = SeoulLegacyTransaction
    legacy_unsigned = SeoulUnsignedLegacyTransaction