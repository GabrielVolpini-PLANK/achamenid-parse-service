from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse

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
        spo2, bpm, pi, isPhysiological = handle_data(data)
        return {"spo2": spo2, "bpm": bpm, "pi": pi, "isPhysiological": isPhysiological}
    except Exception as e:
        return JSONResponse(status_code=422, content={"message": str(e)})
