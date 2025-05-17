from collections.abc import Generator
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright, Page
import shutil
import tomllib


@pytest.fixture
def page() -> Generator[Page, None, None]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        _page = browser.new_page()
        yield _page


@pytest.fixture(autouse=True, scope="session")
def path_for_failed_test_screenshot() -> Generator[Path, None, None]:
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    failed_screenshots_dir = Path(data["project"]["failed_screenshots_dir"])
    if failed_screenshots_dir.exists():
        shutil.rmtree(failed_screenshots_dir)
    failed_screenshots_dir.mkdir(exist_ok=True)
    yield failed_screenshots_dir


@pytest.fixture(autouse=True)
def failed_test_screenshot(
    request: pytest.FixtureRequest, page: Page, path_for_failed_test_screenshot: Path
) -> Generator[None, None, None]:
    yield
    if request.node.rep_call.failed:
        page.screenshot(
            path=path_for_failed_test_screenshot.joinpath(f"{request.node.name}.png")
        )
