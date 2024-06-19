from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Union

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}