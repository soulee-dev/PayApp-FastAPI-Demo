from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import sqlite3
from ..repositories import list_products, create_product

router = APIRouter()


def get_conn() -> sqlite3.Connection:
    from ..main import conn

    return conn


class Product(BaseModel):
    id: int
    name: str
    price: int


class CreateProductIn(BaseModel):
    name: str
    price: int


@router.get("/products", response_model=List[Product])
def get_products(conn: sqlite3.Connection = Depends(get_conn)):
    rows = list_products(conn)
    return [Product(id=r["id"], name=r["name"], price=r["price"]) for r in rows]


@router.post("/products", response_model=Product)
def add_product(inp: CreateProductIn, conn: sqlite3.Connection = Depends(get_conn)):
    if inp.price < 0:
        raise HTTPException(400, "가격은 0 이상이어야 합니다.")
    pid = create_product(conn, inp.name, inp.price)
    return Product(id=pid, name=inp.name, price=inp.price)
