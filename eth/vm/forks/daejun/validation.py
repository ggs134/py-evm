# validation구현해야됨

# frontier -> homestead

# frontier validation주요 로직
# 1) (수수료 + 전송금액)과 잔액 비교
# 2) 논스 확인

# homestead에 포함된 내용
# 3) 서명값 s확인

from eth_utils import (
    ValidationError,
)

from eth.constatns import (
    SECPK1_N,
)

from eth.abc import (
    SignedTransactionAPI,
    StateAPI
)

def validate_daejun_transaction(state : StateAPI,
                                transaction: SignedTransactionAPI) -> None:

    ## homesated logic ##
    
    if transaction.s > SECPK1_N // 2 or transaction.s == 0:
        raise ValidationError("Invalid signature S value")

    ## frontier logic ##

    # gas_cost = transaction.gas * transaction.gas_price
    sender_balance = state.get_balance(transaction.sender)

    # if sender_balance < gas_cost:
    #     raise ValidationError(
    #         f"Sender {transaction.sender!r} cannot afford txn gas "
    #         f"{gas_cost} with account balance {sender_balance}"
    #     )

    # total_cost = transaction.value + gas_cost
    total_cost = transaction.value

    if sender_balance < total_cost:
        raise ValidationError("Sender account balance cannot afford txn")

    sender_nonce = state.get_nonce(transaction.sender)
    if sender_nonce != transaction.nonce:
        raise ValidationError(
            f"Invalid transaction nonce: Expected {sender_nonce}, but got {transaction.nonce}"
        )