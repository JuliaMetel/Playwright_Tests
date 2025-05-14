import pytest
from playwright.sync_api import Page, expect
from utils import wait_page_stable, is_elements_screenshots_equal
from page_one import PageOne
from page_two import PageTwo

class TestClass:

    @pytest.mark.parametrize("sex", ['element_doll_base_male', 'element_doll_base_female'])
    def test_gender_selection_sex(self, page: Page, sex):
        page_one = PageOne(page)
        expect(page_one.element_loading_menu).to_be_visible()
        getattr(page_one, sex).click()
        expect(page_one.element_loading_menu).to_have_class("popupMenu hide")
        expect(page_one.element_loading_menu).not_to_be_visible()
        wait_page_stable(page)

    def test_loading_menu_header_welcome(self, page: Page):
        page_one = PageOne(page)
        expect(page_one.element_loading_menu_welcome).to_have_text(page_one.welcome_text)

    def test_loading_menu_header_select(self, page: Page):
        page_one = PageOne(page)
        expect(page_one.element_loading_menu_select).to_have_text(page_one.select_text)

    @pytest.mark.parametrize("sex", ['element_doll_base_male', 'element_doll_base_female'])
    def test_decals_head_1(self, page: Page, sex):
        page_one = PageOne(page)
        getattr(page_one, sex).click()
        page_two = PageTwo(page)
        wait_page_stable(page)
        page_two.element_eye.click()
        page_two.element_head_1.click()
        wait_page_stable(page)
        assert is_elements_screenshots_equal(f'./{sex}_true.png',page_two.element_canvas, sex), "Screenshots don't match"