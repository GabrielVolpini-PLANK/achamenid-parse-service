from pydantic import BaseModel


class SensorData(BaseModel):
    ir: str
    red: str
    timestamp: str
