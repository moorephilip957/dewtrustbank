from dataclasses import dataclass


@dataclass
class TransactionResult:
    status: str
    message: str
    transaction: object