from pydantic import BaseModel


class SensorData(BaseModel):
    ir: int
    red: int
    timestamp: str
