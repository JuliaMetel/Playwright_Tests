import time
from typing import Callable
import pytest
from PIL.ImageFile import ImageFile
from playwright.sync_api import expect, Page, Route, Request
from utils import wait_page_stable, is_elements_screenshots_equal
from page_one import PageOne
from page_two import PageTwo
from page_three import PageThree
from page_four import PageFour
from page_five import PageFive


class TestClass:
    @pytest.mark.parametrize(
        "sex", ["element_doll_base_female", "element_doll_base_male"]
    )
    def test_gender_selection_sex(self, page: Page, sex: str) -> None:
        page_one = PageOne(page)
        expect(page_one.element_loading_menu).to_have_class("popupMenu")
        getattr(page_one, sex).click()
        expect(page_one.element_loading_menu).to_have_class("popupMenu hide")
        wait_page_stable(page)

    def test_loading_menu_header_welcome(self, page: Page) -> None:
        page_one = PageOne(page)
        expect(page_one.element_loading_menu_welcome).to_have_text(
            page_one.welcome_text
        )

    def test_loading_menu_header_select(self, page: Page) -> None:
        page_one = PageOne(page)
        expect(page_one.element_loading_menu_select).to_have_text(page_one.select_text)

    @pytest.mark.parametrize(
        "sex", ["element_doll_base_male", "element_doll_base_female"]
    )
    def test_decals_head_1(
        self, page: Page, sex: str, get_screenshot: Callable[[str], ImageFile]
    ) -> None:
        page_one = PageOne(page)
        getattr(page_one, sex).click()
        page_two = PageTwo(page)
        wait_page_stable(page)
        page_two.element_eye.click()
        page_two.element_head_1.click()
        wait_page_stable(page)
        time.sleep(5)
        assert is_elements_screenshots_equal(
            get_screenshot(sex), page_two.element_canvas
        ), "Screenshots don't match"

    @pytest.mark.parametrize(
        "sex", ["element_doll_base_male", "element_doll_base_female"]
    )
    def test_turning_canvas(
        self, page: Page, sex: str, get_screenshot: Callable[[str], ImageFile]
    ) -> None:
        page_one = PageOne(page)
        expect(page_one.element_loading_menu).to_have_class("popupMenu")
        getattr(page_one, sex).click()
        expect(page_one.element_loading_menu).to_have_class("popupMenu hide")
        wait_page_stable(page)
        page_two = PageTwo(page)
        page_two.element_canvas.hover()
        box = page_two.element_canvas.bounding_box()
        assert box is not None, "Taking box from absent/not visible element"
        page.mouse.down(button="left")
        page.mouse.move(box["x"] + 1, box["y"] + 1, steps=15)
        page.mouse.up(button="left")
        time.sleep(5)
        assert is_elements_screenshots_equal(
            get_screenshot(sex), page_two.element_canvas
        ), "Screenshots don't match"


class TestClassAJAX:
    def test_spinner_with_network_settings(self, page: Page) -> None:
        page_three = PageThree(page)
        expect(page_three.spinner).not_to_be_visible()
        page.context.new_cdp_session(page).send(
            "Network.emulateNetworkConditions",
            {
                "downloadThroughput": ((500 * 1000) / 8) * 0.2,
                "uploadThroughput": ((500 * 1000) / 8) * 0.2,
                "latency": 400 * 50,
                "offline": False,
            },
        )
        page_three.button_triggering_ajax_request.click()
        expect(page_three.spinner).to_be_visible()

    def test_spinner_with_route(self, page: Page) -> None:
        page_three = PageThree(page)
        expect(page_three.spinner).not_to_be_visible()

        def handle(route: Route):
            expect(page_three.spinner).to_be_visible()
            route.continue_()

        page.route("**/ajaxdata", handle)
        page_three.button_triggering_ajax_request.click()

    def test_text_by_request(self, page: Page) -> None:
        text = "None"
        page_three = PageThree(page)
        expect(page_three.spinner).not_to_be_visible()

        def handle(route: Route, request: Request):
            expect(page_three.spinner).to_be_visible()
            import requests

            resp = requests.get(request.url)
            nonlocal text
            text = resp.text
            route.fulfill(
                status=resp.status_code, body=resp.text, headers=dict(resp.headers)
            )

        page.route("**/ajaxdata", handle)
        page_three.button_triggering_ajax_request.click()
        expect(page_three.spinner).not_to_be_visible(timeout=100000)
        expect(page_three.content).to_have_text(text)

    def test_text_by_changed_request(self, page: Page) -> None:
        page_three = PageThree(page)
        expect(page_three.spinner).not_to_be_visible()

        def handle(route: Route, request: Request):
            expect(page_three.spinner).to_be_visible()
            import requests

            resp = requests.get(request.url)
            route.fulfill(
                status=resp.status_code,
                body="New text here",
                headers=dict(resp.headers),
            )

        page.route("**/ajaxdata", handle)
        page_three.button_triggering_ajax_request.click()
        expect(page_three.spinner).not_to_be_visible(timeout=100000)
        expect(page_three.content).to_have_text("New text here")


class TestClassQAPlayground:
    def test_button_in_iframe(self, page: Page) -> None:
        page_four = PageFour(page)
        page_four.button.click()
        expect(page_four.text_by_button()).to_have_text("Button Clicked")

    def test_upload_file(self, page: Page) -> None:
        page_five = PageFive(page)
        expect(page_five.text_under_button()).to_have_text("No File Selected")
        with page.expect_file_chooser() as fc_info:
            page_five.button_select_image_file.click()
        file_chooser = fc_info.value
        file_chooser.set_files("./pictures/test_pic.jpg")
        expect(page_five.text_under_button()).to_have_text("1 File Selected")
