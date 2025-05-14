from playwright.sync_api import Page


class PageOne():
    link = "https://webglsamples.org/collectibles/index.html"
    welcome_text = 'Welcome to Collectibles Painter'
    select_text = 'Select a model to begin'

    def __init__(self, page: Page):
        self.page = page
        page.goto(self.link)

    @property
    def element_loading_menu(self):
        return self.page.locator("css=.popupMenu")

    @property
    def element_doll_base_female(self):
        return self.page.get_by_alt_text("Female Doll", exact=True)

    @property
    def element_doll_base_male(self):
        return self.page.get_by_alt_text("Male Doll", exact=True)

    @property
    def element_loading_menu_welcome(self):
        return self.page.locator('#loadingMenu h4')

    @property
    def element_loading_menu_select(self):
        return self.page.locator('//*[@id="loadingMenu"]/h2')