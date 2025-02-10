from sqlalchemy import Column, String, Boolean
from app.models.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ModerationResult(Base):
    text = Column(String, nullable=False)
    result = Column(Boolean, nullable=False)
    meta = Column(JSONB, nullable=True)
