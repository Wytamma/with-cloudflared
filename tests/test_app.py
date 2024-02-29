from typing import Union
from with_cloudflared import cloudflared
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    port = 8000
    with cloudflared(port=port) as cloudflared_address:
        print(f" * Running on {cloudflared_address}")
        uvicorn.run(app)