from playwright.sync_api import sync_playwright
from constants import device_list, browser_list
from models import *

import base64


class BrowserActions:
    def __init__(self, browser: str = "chromium") -> None:
        pass

    def take_screenshot(self, data: ScreenshotRequest):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                color_scheme=data.color_scheme, **(data.device if data.device else {})
            )
            page = context.new_page()
            page.goto(str(data.url))
            if data.locator:
                screenshot_bytes = page.locator(data.locator).screenshot(
                    full_page=data.full_page
                )
            else:
                screenshot_bytes = page.screenshot(full_page=data.full_page)
        data = base64.b64encode(screenshot_bytes).decode()
        return data

    def generate_pdf(self, data: PdfRequest):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(str(data.url))
            page.emulate_media()
            pdf_bytes = page.pdf(format=data.format)
        return base64.b64encode(pdf_bytes).decode()

    def scrape_content(self, data: ScrapeRequest):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                **({"user_agent": data.user_agent} if data.user_agent else {})
            )
            page = context.new_page()
            page.goto(str(data.url))
            if data.locator:
                content = page.locator(data.locator).evaluate(
                    "element => element.outerHTML"
                )
            else:
                content = page.content()
        return content
