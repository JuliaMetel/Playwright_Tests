from collections.abc import Generator
from typing import Any
import pytest
from playwright.sync_api import sync_playwright, Page


@pytest.fixture
def page(request: pytest.FixtureRequest) -> Generator[Any, Any, Page]:
    with sync_playwright() as playwright:
        Browser = playwright.chromium.launch(headless=False)
        page = Browser.new_page()
        yield page


@pytest.fixture(autouse=True)
def failed_test_screenshot(request: pytest.FixtureRequest, page):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"{request.node.name}.png")
