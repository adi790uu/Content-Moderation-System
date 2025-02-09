from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func
import cuid


@as_declarative()
class Base:
    cuid = Column(
        String(25),
        primary_key=True,
        default=cuid.cuid,
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
