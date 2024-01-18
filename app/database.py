from abc import ABC, abstractmethod
from typing import Dict, List

from beanie import init_beanie
from config import settings
from models import Product
from motor.motor_asyncio import AsyncIOMotorClient


class AddProductBase(ABC):
    @abstractmethod
    def add(self, db_model, data: Dict[str, str]) -> None:
        pass

    @abstractmethod
    def add_all(self, db_model, data: List[Dict[str, str]]) -> None:
        pass


class AddProductMongo:
    def __init__(self):
        self._mongo_client = AsyncIOMotorClient(
            settings.MONGO_HOST.get_secret_value(),
            int(settings.MONGO_PORT.get_secret_value()),
            username=settings.MONGO_USER.get_secret_value(),
            password=settings.MONGO_PASSWORD.get_secret_value(),
        )

        self.db_product = None

    async def open_connection(self):
        await init_beanie(database=self._mongo_client[settings.MONGO_DB.get_secret_value()], document_models=[Product])

    def close_connection(self):
        self._mongo_client.close()

    async def add(self, item: Dict[str, str]):
        await Product(title=item["title"], link=item["link"], description=item["description"]).create()

    async def add_all(self, items: List[Dict[str, str]]):
        for item in items:
            await Product(title=item["title"], link=item["link"], description=item["description"]).create()


def addProduct() -> AddProductBase:
    return AddProductMongo()
