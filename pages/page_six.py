from utils import wait_page_stable
from playwright.sync_api import Page, Locator


class PageSix:
    link = "https://qaplayground.dev/apps/popup/#/"

    def __init__(self, page: Page) -> None:
        self.page = page
        page.goto(self.link, timeout=0)
        wait_page_stable(page)

    @property
    def button_open(self) -> Locator:
        return self.page.locator("css=.btn")
