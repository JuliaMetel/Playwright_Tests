from utils import wait_page_stable
from playwright.sync_api import Page, Locator


class PageFour:
    link = "https://qaplayground.dev/apps/iframe/"

    def __init__(self, page: Page) -> None:
        self.page = page
        page.goto(self.link, timeout=0)
        wait_page_stable(page)

    @property
    def button(self) -> Locator:
        return self.page.frame_locator("css=#frame1").frame_locator("css=#frame2").locator("css=.btn")

    def text_by_button(self) -> Locator:
        return self.page.frame_locator("css=#frame1").frame_locator("css=#frame2").locator("css=#msg")