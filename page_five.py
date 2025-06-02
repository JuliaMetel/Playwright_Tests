from utils import wait_page_stable
from playwright.sync_api import Page, Locator


class PageFive:
    link = "https://qaplayground.dev/apps/upload/"

    def __init__(self, page: Page) -> None:
        self.page = page
        page.goto(self.link, timeout=0)
        wait_page_stable(page)

    @property
    def button_select_image_file(self) -> Locator:
        return self.page.locator("css=.btn-green-outline")

    def text_under_button(self) -> Locator:
        return self.page.locator("css=#num-of-files")

