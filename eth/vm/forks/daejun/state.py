from typing import Type

from eth_hash.auto import keccak

from eth_utils import (
    encode_hex,
)

from eth._utils.address import (
    generate_contract_address,
)

from eth.vm.forks.berlin.state import (
    BerlinState,
)

from eth.vm.message import (
    Message,
)

from eth.vm.forks.berlin.state import (
    BerlinTransactionExecutor,
)

from eth.abc import (
    ComputationAPI,
    MessageAPI,
    SignedTransactionAPI,
    TransactionExecutorAPI,
)

from eth.constants import CREATE_CONTRACT_ADDRESS
from eth.vm.forks.frontier.constants import REFUND_SELFDESTRUCT

from .computation import DaejunComputation

from .validation import validate_daejun_transaction


class DaejunTransactionExecutor(BerlinTransactionExecutor):

    ## Executor() 동작 순서 ##

    # def build_evm_message():
    #     # 가스 차감 후 메시지 객체 생성[frontier코드 참조]
    #     pass

    # def build_computation():
    #     # VM연산 수행[frontier코드 참조, berlin으로 상속방법 참조]
    #     # computation : apply_create_message() or apply_message() [frontier코드 참조]
    #     # -> apply_computaion() : loop연산 (메모리, 스택, 리턴 등), 상태 commit [base코드 참조]
    #     pass

    # def finalize_computation():
    #     # 가스 환불(refuld)[frontier코드 참조]
    #     # 트랜잭션 실사용 가스 계산, 마이너에게 지급(coinbase상태값에 반영)
    #     pass

    def build_evm_message(self, transaction: SignedTransactionAPI) -> MessageAPI:

        ### DAEJUN changed ###
        # gas_fee = transaction.gas * transaction.gas_price
        gas_fee = 0

        ### DAEJUN changed ###
        # Buy Gas
        self.vm_state.delta_balance(transaction.sender, -1 * gas_fee)

        # Increment Nonce
        self.vm_state.increment_nonce(transaction.sender)

        # Setup VM Message
        # VM에 최초로 전달하는 가스량. 그냥 두면 된다.
        message_gas = transaction.gas - transaction.intrinsic_gas

        if transaction.to == CREATE_CONTRACT_ADDRESS:
            contract_address = generate_contract_address(
                transaction.sender,
                self.vm_state.get_nonce(transaction.sender) - 1,
            )
            data = b''
            code = transaction.data
        else:
            contract_address = None
            data = transaction.data
            code = self.vm_state.get_code(transaction.to)

        self.vm_state.logger.debug2(
            (
                "TRANSACTION: sender: %s | to: %s | value: %s | gas: %s | "
                "gas-price: %s | s: %s | r: %s | y_parity: %s | data-hash: %s"
            ),
            encode_hex(transaction.sender),
            encode_hex(transaction.to),
            transaction.value,
            transaction.gas,
            transaction.gas_price,
            transaction.s,
            transaction.r,
            transaction.y_parity,
            encode_hex(keccak(transaction.data)),
        )

        message = Message(
            gas=message_gas,
            to=transaction.to,
            sender=transaction.sender,
            value=transaction.value,
            data=data,
            code=code,
            create_address=contract_address,
        )
        return message

    def finalize_computation(self,
                             transaction: SignedTransactionAPI,
                             computation: ComputationAPI) -> ComputationAPI:

        # Self Destruct Refunds
        num_deletions = len(computation.get_accounts_for_deletion())
        if num_deletions:
            computation.refund_gas(REFUND_SELFDESTRUCT * num_deletions)

        # Gas Refunds
        gas_remaining = computation.get_gas_remaining()
        gas_refunded = computation.get_gas_refund()
        gas_used = transaction.gas - gas_remaining
        gas_refund = min(gas_refunded, gas_used // 2)
        gas_refund_amount = (gas_refund + gas_remaining) * transaction.gas_price

        if gas_refund_amount:
            self.vm_state.logger.debug2(
                'TRANSACTION REFUND: %s -> %s',
                gas_refund_amount,
                encode_hex(computation.msg.sender),
            )

            # self.vm_state.delta_balance(computation.msg.sender, gas_refund_amount)

        ### DAEJUN changed ###
        # Miner Fees
        # transaction_fee = \
        #     (transaction.gas - gas_remaining - gas_refund) * transaction.gas_price
        transaction_fee = 0
        self.vm_state.logger.debug2(
            'TRANSACTION FEE: %s -> %s',
            transaction_fee,
            encode_hex(self.vm_state.coinbase),
        )
        self.vm_state.delta_balance(self.vm_state.coinbase, transaction_fee)

        # Process Self Destructs
        for account, _ in computation.get_accounts_for_deletion():
            # TODO: need to figure out how we prevent multiple selfdestructs from
            # the same account and if this is the right place to put this.
            self.vm_state.logger.debug2('DELETING ACCOUNT: %s', encode_hex(account))

            # TODO: this balance setting is likely superflous and can be
            # removed since `delete_account` does this.
            self.vm_state.set_balance(account, 0)
            self.vm_state.delete_account(account)

        return computation


class DaejunState(BerlinState):
    
    # executor.__call__()의 동작 순서[base computation.py]
    # (1) validate_transaction(transaction)
    # (2) build_evm_message(transaction)
    # (3) build_computation(message, transaction)
    # (4) finalize_computation(transaction, computation)
    # (5) return finalized_computation    

    computation_class = DaejunComputation
    transaction_executor_class: Type[TransactionExecutorAPI] = DaejunTransactionExecutor

    def validate_transaction(self, transaction: SignedTransactionAPI) -> None:
        validate_daejun_transaction(self, transaction)

