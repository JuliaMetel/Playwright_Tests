from utils import wait_page_stable
from playwright.sync_api import Page, Locator


class PageOne:
    link = "https://webglsamples.org/collectibles/index.html"
    welcome_text = "Welcome to Collectibles Painter"
    select_text = "Select a model to begin"

    def __init__(self, page: Page) -> None:
        self.page = page
        page.goto(self.link, timeout=0)
        wait_page_stable(page)

    @property
    def element_loading_menu(self) -> Locator:
        return self.page.locator("css=.popupMenu")

    @property
    def element_doll_base_female(self) -> Locator:
        return self.page.get_by_alt_text("Female Doll", exact=True)

    @property
    def element_doll_base_male(self) -> Locator:
        return self.page.get_by_alt_text("Male Doll", exact=True)

    @property
    def element_loading_menu_welcome(self) -> Locator:
        return self.page.locator("#loadingMenu h4")

    @property
    def element_loading_menu_select(self) -> Locator:
        return self.page.locator('//*[@id="loadingMenu"]/h2')
