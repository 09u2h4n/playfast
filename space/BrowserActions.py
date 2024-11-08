import base64
from playwright.sync_api import sync_playwright
from constants import browser_list

class BrowserActions:
    def __init__(self, browser: str = "chromium"):
        if browser not in browser_list:
            raise ValueError(f"Browser {browser} is not supported. Supported browsers are: {browser_list}")
        self.browser_type = browser
        self.playwright = sync_playwright().start()
        self.browser = self.playwright[self.browser_type].launch()

    def __del__(self):
        # Clean up the browser instance
        self.browser.close()
        self.playwright.stop()

    def take_screenshot(self, url: str, device: str = None, color_scheme: str = "light", full_page: bool = True, locator: str = None) -> str:
        with self.browser.new_context(**(self.browser.devices[device] if device else {})) as context:
            page = context.new_page(color_scheme=color_scheme)
            page.goto(url)
            image_data = page.locator(locator).screenshot() if locator else page.screenshot(full_page=full_page)
            return base64.b64encode(image_data).decode()

    def generate_pdf(self, url: str, format: str = "A4"):
        with self.browser.new_context() as context:
            page = context.new_page()
            page.goto(url)
            page.emulate_media()  # Optional, for print layout
            pdf_data = page.pdf(format=format)
            return pdf_data

    def scrape_data(self, url: str, locator: str = None, user_agent: str = None):
        with self.browser.new_context(user_agent=user_agent if not user_agent is None else None) as context:
            page = context.new_page()
            page.goto(url)
            data = page.locator(locator).evaluate("element => element.outerHTML") if locator else page.content()
            return data

    