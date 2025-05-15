class PageTwo:
    def __init__(self, page):
        self.page = page

    @property
    def element_canvas(self):
        return self.page.locator("css=#canvas")

    @property
    def element_eye(self):
        return self.page.locator("css=#eye")

    @property
    def element_head_1(self):
        return self.page.locator("css=#head_1")
