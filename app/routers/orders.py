from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from ..models import CreateOrderIn, CreateOrderOut
from ..config import PAYAPP_USERID, SHOP_NAME, BASE_URL
from ..repositories import get_product, create_order, get_order
import sqlite3

router = APIRouter()


def get_conn() -> sqlite3.Connection:
    from ..main import conn  # 전역 커넥션 재사용

    return conn


@router.post("/orders", response_model=CreateOrderOut)
def create_order_route(
    inp: CreateOrderIn, conn: sqlite3.Connection = Depends(get_conn)
):
    p = get_product(conn, inp.product_id)
    if not p:
        raise HTTPException(404, "상품이 존재하지 않습니다.")
    amount = int(p["price"])
    order_id = create_order(conn, p["id"], amount)
    return CreateOrderOut(
        order_id=order_id,
        product_name=p["name"],
        amount=amount,
        userid=PAYAPP_USERID,
        shopname=SHOP_NAME,
        feedbackurl=f"{BASE_URL}/webhook",
        returnurl=f"{BASE_URL}/result?order_id={order_id}",
    )


@router.post("/result", response_class=PlainTextResponse)
def result(order_id: str, conn: sqlite3.Connection = Depends(get_conn)):
    row = get_order(conn, order_id)
    if not row:
        return PlainTextResponse("주문을 찾을 수 없습니다.", status_code=404)
    return f"[{row['id']}] 현재 상태: {row['status']} / 금액: {row['amount']}원"
