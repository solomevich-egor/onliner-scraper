from abc import ABC, abstractmethod
from typing import Dict

from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class BaseScraper(ABC):
    @abstractmethod
    def get_page_data(self, xpath: Dict[str, str]):
        pass


class OnlinerScraper(BaseScraper):
    def __init__(self, target_link: str):
        firefox_options = Options()
        firefox_options.headless = True
        self._driver = webdriver.Firefox(options=firefox_options)
        self._target_link = target_link

    def get_page_data(self, xpath: Dict[str, str]):
        self._driver.get(self._target_link)
        html = self._driver.page_source
        page_selector = Selector(text=html)
        self._driver.close()

        goods = list()
        for item in page_selector.xpath(xpath["item"]):
            good = {}
            for category in xpath["fields"]:
                good[category] = (Selector(text=item.extract()).xpath(xpath["fields"][category]).extract_first()).strip(
                    " \n"
                )
            goods.append(good)

        return goods


def get_scraper(url: str):
    return OnlinerScraper(target_link=url)
