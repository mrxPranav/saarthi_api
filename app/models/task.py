from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    text = Column(String, nullable=True)
    title = Column(String, nullable=True)
    status = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    date_time = Column(DateTime(timezone=True), server_default=func.now())
