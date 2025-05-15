import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page(request):
    with sync_playwright() as Page:
        Browser = Page.chromium.launch(headless=False)
        page = Browser.new_page()
        yield page
