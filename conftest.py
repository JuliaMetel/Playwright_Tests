from collections.abc import Generator
import pytest
from playwright.sync_api import sync_playwright, Page


@pytest.fixture
def page() -> Generator[Page, None, None]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        _page = browser.new_page()
        yield _page


@pytest.fixture(autouse=True)
def failed_test_screenshot(request: pytest.FixtureRequest, page: Page):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"{request.node.name}.png")
