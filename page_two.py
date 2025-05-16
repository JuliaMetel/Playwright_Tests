from playwright.sync_api import Page, Locator

class PageTwo:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def element_canvas(self) -> Locator:
        return self.page.locator("css=#canvas")

    @property
    def element_eye(self) -> Locator:
        return self.page.locator("css=#eye")

    @property
    def element_head_1(self) -> Locator:
        return self.page.locator("css=#head_1")
