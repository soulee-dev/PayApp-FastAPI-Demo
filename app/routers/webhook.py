from typing import Annotated, Optional
from fastapi import APIRouter, Form, Depends
from fastapi.responses import PlainTextResponse
from ..models import PayState
from ..config import PAYAPP_USERID, PAYAPP_LINKKEY, PAYAPP_LINKVAL
from ..repositories import get_order, update_order_status
import sqlite3

router = APIRouter()


def get_conn() -> sqlite3.Connection:
    from ..main import conn

    return conn


def verify_seller(userid: str, linkkey: str, linkval: str) -> bool:
    return (
        userid == PAYAPP_USERID
        and linkkey == PAYAPP_LINKKEY
        and linkval == PAYAPP_LINKVAL
    )


@router.post("/webhook", response_class=PlainTextResponse)
async def webhook(
    userid: Annotated[str, Form()],
    linkkey: Annotated[str, Form()],
    linkval: Annotated[str, Form()],
    price: Annotated[int, Form()],
    pay_state: Annotated[int, Form()],
    var1: Annotated[Optional[str], Form()] = None,
    conn: sqlite3.Connection = Depends(get_conn),
):
    try:
        if not verify_seller(userid, linkkey, linkval):
            print("[WEBHOOK] invalid seller")
            return "SUCCESS"

        order_id = var1
        if not order_id:
            print("[WEBHOOK] missing order_id(var1)")
            return "SUCCESS"

        order = get_order(conn, order_id)
        if not order:
            print(f"[WEBHOOK] not found order {order_id}")
            return "SUCCESS"

        if int(order["amount"]) != int(price):
            print(f"[WEBHOOK] amount mismatch: db={order['amount']} webhook={price}")
            return "SUCCESS"

        state = PayState(pay_state)
        if state == PayState.COMPLETED:
            update_order_status(conn, order_id, "결제완료")
            print(f"[WEBHOOK] 결제완료 처리: {order_id}")
        elif state in (
            PayState.CANCEL_REQUEST,
            PayState.CANCEL_REQUEST_ALT,
            PayState.CANCEL_APPROVED,
            PayState.CANCEL_APPROVED_ALT,
        ):
            update_order_status(conn, order_id, "결제취소")
            print(f"[WEBHOOK] 결제취소 처리: {order_id}")
        elif state in (PayState.PARTIAL_CANCEL, PayState.PARTIAL_CANCEL_ALT):
            update_order_status(conn, order_id, "부분취소")
            print(f"[WEBHOOK] 부분취소 처리: {order_id}")
        elif state == PayState.PENDING:
            update_order_status(conn, order_id, "결제대기")
            print(f"[WEBHOOK] 결제대기 처리: {order_id}")
        else:
            print(f"[WEBHOOK] ignore state={state} for order={order_id}")

        return "SUCCESS"

    except Exception as e:
        print("[WEBHOOK][ERROR]", e)
        return "SUCCESS"
