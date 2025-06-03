from utils import wait_page_stable
from playwright.sync_api import Page


class PageSix:
    link = "https://qaplayground.dev/apps/popup/#/"

    def __init__(self, page: Page) -> None:
        self.page = page
        page.goto(self.link, timeout=0)
        wait_page_stable(page)
