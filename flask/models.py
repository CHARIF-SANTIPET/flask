from __future__ import annotations
from typing import List

from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

from .database import Base


class Receiver(Base):
    __tablename__ = "receivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    phone_number = Column(String, index=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(
    #     DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    # )
    item: Mapped[List["Item"]] = relationship(back_populates="receiver")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    weight = Column(Numeric(8, 3), nullable=True)
    description = Column(String, index=True)
    service_price = Column(Numeric(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    receiver_id: Mapped[int] = mapped_column(ForeignKey("receivers.id"))
    receiver: Mapped["Receiver"] = relationship(back_populates="item")
