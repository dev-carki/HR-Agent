from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from backend.services.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255))
    phone = Column(String(20))
    resume_path = Column(String(500))
    photo_path = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
