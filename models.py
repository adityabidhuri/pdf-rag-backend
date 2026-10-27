from sqlalchemy import Integer,String,ForeignKey, DateTime
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class User(Base):
    __tablename__="users"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    email:Mapped[str]=mapped_column(String,unique=True,index=True,nullable=False)
    hashed_password:Mapped[str]=mapped_column(String,nullable=False)

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )