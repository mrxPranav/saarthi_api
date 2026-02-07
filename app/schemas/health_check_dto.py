from pydantic import BaseModel
from datetime import datetime

class HealthCheckBase(BaseModel):
    request_time: datetime
    response_time: datetime
    difference: float
    status: str

class HealthCheckCreate(HealthCheckBase):
    pass

class HealthCheckResponse(HealthCheckBase):
    id: int

    class Config:
        from_attributes = True
