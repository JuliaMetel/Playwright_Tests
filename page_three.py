from utils import wait_page_stable
from playwright.sync_api import Page, Locator


class PageThree:
    link = "http://uitestingplayground.com/ajax"

    def __init__(self, page: Page) -> None:
        self.page = page
        page.goto(self.link, timeout=0)
        wait_page_stable(page)

    @property
    def button_triggering_ajax_request(self) -> Locator:
        return self.page.locator("css=#ajaxButton")

    @property
    def spinner(self) -> Locator:
        return self.page.locator("css=#spinner")

    @property
    def content(self) -> Locator:
        return self.page.locator("css=#content")
