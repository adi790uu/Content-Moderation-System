from sqlalchemy import Column, String
from app.models.base import Base


class ModerationResult(Base):
    text = Column(String, nullable=False)
    result = Column(String, nullable=False)
