from typing import List

from fastapi import FastAPI

from extractor import handle_data
from models import SensorData

app = FastAPI()


@app.get("/")
@app.post("/")
@app.put("/")
def read_root():
    print("GET request received at root endpoint")
    return {"Hello": "World"}


@app.post("/parse")
async def parse(data: List[SensorData]):
    try:
        spo2, bpm, pi = handle_data(data)
        return {"spo2": spo2, "bpm": bpm, "pi": pi}
    except Exception as e:
        return {"data": data, "error": str(e)}
