import asyncio
import json

from database import addProduct
from scrapers import get_scraper


async def main(scrap_url: str):
    with open(scrap_url) as file:
        items = json.load(file)

    add_product = addProduct()
    await add_product.open_connection()
    tasks = list()
    for item in items:
        tasks.append(asyncio.create_task(add_product.add_all(get_scraper(item).get_page_data(items[item]))))

    for task in tasks:
        await task

    add_product.close_connection()


if __name__ == "__main__":
    url = "app/onliner.json"
    asyncio.run(main(url))
