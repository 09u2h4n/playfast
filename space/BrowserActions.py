import base64
from playwright.async_api import async_playwright
from constants import browser_list

class BrowserActions:
    def __init__(self, browser: str = "chromium"):
        if browser not in browser_list:
            raise ValueError(f"Browser {browser} is not supported. Supported browsers are: {browser_list}")
        self.browser_type = browser
        self.playwright = None
        self.browser = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright[self.browser_type].launch()

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def take_screenshot(self, url: str, device: str = None, color_scheme: str = "light", full_page: bool = True, locator: str = None) -> str:
        async with self.browser.new_context(**(self.playwright.devices[device] if device else {})) as context:
            page = await context.new_page()
            await page.goto(url)
            image_data = await page.locator(locator).screenshot() if locator else await page.screenshot(full_page=full_page)
            return base64.b64encode(image_data).decode()

    async def generate_pdf(self, url: str, format: str = "A4"):
        async with self.browser.new_context() as context:
            page = await context.new_page()
            await page.goto(url)
            await page.emulate_media()  # Optional, for print layout
            pdf_data = await page.pdf(format=format)
            return pdf_data

    async def scrape_data(self, url: str, locator: str = None, user_agent: str = None):
        async with self.browser.new_context(user_agent=user_agent if user_agent else None) as context:
            page = await context.new_page()
            await page.goto(url)
            data = await page.locator(locator).evaluate("element => element.outerHTML") if locator else await page.content()
            return data
