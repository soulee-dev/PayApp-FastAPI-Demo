from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .db import connect, init_db
from .routers import orders, webhook, products

app = FastAPI()

conn = connect()
init_db(conn)

# 라우터 등록
app.include_router(orders.router)
app.include_router(webhook.router)
app.include_router(products.router)

# 정적 파일/루트
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")
