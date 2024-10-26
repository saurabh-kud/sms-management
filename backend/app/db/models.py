from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
import datetime
import json
from enum import Enum as PyEnum
from typing import Any
from typing import List
from typing import Literal
from typing import Optional
from typing import TypedDict
from typing_extensions import NotRequired
import uuid

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy import JSON
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship




class Base(DeclarativeBase):
    pass




class User( Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True,nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    email : Mapped[str] = mapped_column(String, nullable=False,unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

