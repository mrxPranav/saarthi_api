from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.config.database import Base

class HealthCheck(Base):
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    request_time = Column(DateTime(timezone=True), nullable=False)
    response_time = Column(DateTime(timezone=True), nullable=False)
    difference = Column(Float, nullable=False) # Difference in seconds
    status = Column(String, nullable=False)
