from enum import IntEnum
from pydantic import BaseModel


class PayState(IntEnum):
    REQUEST = 1
    COMPLETED = 4
    CANCEL_REQUEST = 8
    CANCEL_REQUEST_ALT = 32
    CANCEL_APPROVED = 9
    CANCEL_APPROVED_ALT = 64
    PENDING = 10
    PARTIAL_CANCEL = 70
    PARTIAL_CANCEL_ALT = 71


class CreateOrderIn(BaseModel):
    product_id: int


class CreateOrderOut(BaseModel):
    order_id: str
    product_name: str
    amount: int
    userid: str
    shopname: str
    feedbackurl: str
    returnurl: str
