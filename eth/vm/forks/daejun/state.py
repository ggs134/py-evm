from typing import Type

from eth.vm.forks.berlin.state import (
    BerlinState
)

from eth.vm.forks.berlin.state import (
    BerlinTransactionExecutor
)

from eth.abc import (
    ComputationAPI,
    MessageAPI,
    SignedTransactionAPI,
    TransactionExecutorAPI,
)

from .computation import DaejunComputation
from .validation import validate_daejun_transaction


class DaejunTransactionExecutor(BerlinTransactionExecutor):
    def build_evm_message():
        # 가스 차감 후 메시지 객체 생성[frontier코드 참조]
        pass
    def build_computation():
        # VM연산 수행[frontier코드 참조, berlin으로 상속방법 참조]
        # computation : apply_create_message() or apply_message() [frontier코드 참조]
        # -> apply_computaion() : loop연산 (메모리, 스택, 리턴 등), 상태 commit [base코드 참조]
        pass
    def finalize_computation():
        # 가스 환불(refuld)[frontier코드 참조]
        # 트랜잭션 실사용 가스 계산, 마이너에게 지급(coinbase상태값에 반영)
        pass
    pass


class DaejunState(BerlinState):
    computation_class = DaejunComputation
    transaction_executor_class: Type[TransactionExecutorAPI] = DaejunTransactionExecutor

    def validate_transaction(self, transaction: SignedTransactionAPI) -> None:
        validate_daejun_transaction(self, transaction)

