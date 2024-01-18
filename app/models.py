from typing import Optional
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field
from pymongo import IndexModel


class Product(Document):
    uuid: UUID = Field(default_factory=uuid4)
    title: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None

    class Settings:
        indexes = [
            IndexModel("uuid", unique=True),
        ]
