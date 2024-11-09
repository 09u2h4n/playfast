import base64
from playwright.sync_api import sync_playwright, BrowserContext
from constants import browser_list, device_list, pdf_format_list

class BrowserActions:
    def __init__(self, browser_type: str):
        if browser_type not in browser_list:
            raise ValueError(f"{browser_type} is not supported. Supported browsers: {browser_list}")
        self.browser_type = browser_type
        self.playwright = sync_playwright().start()

    def _get_browser_context(self, device_name=None, color_scheme="light"):
        # Choose browser type
        browser = getattr(self.playwright, self.browser_type).launch()
        context = browser.new_context(
            **(self.playwright.devices[device_name] if device_name in device_list else {}),
            color_scheme=color_scheme
        )
        return context, browser

    def take_screenshot(self, url, device=None, full_page=True, color_scheme="light", locator=None):
        context, browser = self._get_browser_context(device_name=device, color_scheme=color_scheme)
        page = context.new_page()
        page.goto(url)

        if locator:
            element = page.locator(locator)
            screenshot = element.screenshot()
        else:
            screenshot = page.screenshot(full_page=full_page)

        context.close()
        browser.close()
        return base64.b64encode(screenshot).decode("utf-8")

    def generate_pdf(self, url, format="A4"):
        if format not in pdf_format_list:
            raise ValueError(f"Invalid format. Supported formats are {pdf_format_list}.")

        context, browser = self._get_browser_context()
        page = context.new_page()
        page.goto(url)
        pdf_data = page.pdf(format=format)

        context.close()
        browser.close()
        return base64.b64encode(pdf_data).decode("utf-8")

    def scrape_data(self, url, locator=None, user_agent=None):
        context, browser = self._get_browser_context()
        page = context.new_page()

        if user_agent:
            context.set_user_agent(user_agent)

        page.goto(url)
        data = page.locator(locator).inner_text() if locator else page.content()

        context.close()
        browser.close()
        return data.encode("utf-8")
