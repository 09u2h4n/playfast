from fastapi import FastAPI
from models import ScreenshotRequest, ScreenshotResponse, PdfRequest, PdfResponse, ScrapeRequests, ScrapeResponse, DeviceListResponse, BrowserListResponse
from tools import dummy_function, measure_time
from BrowserActions import BrowserActions

app = FastAPI(docs_url="/")

@app.post("/screenshot")
@measure_time()
async def take_screenshot(request: ScreenshotRequest):
    browser_action = BrowserActions(browser=request.browser)
    await browser_action.start()  # Start the browser asynchronously
    try:
        data = await browser_action.take_screenshot(
            url=request.url,
            device=request.device,
            color_scheme=request.color_scheme,
            full_page=request.full_page,
            locator=request.locator
        )
        return ScreenshotResponse(data=data).dict()
    finally:
        await browser_action.close()  # Ensure the browser is closed asynchronously

@app.post("/pdf")
@measure_time()
async def generate_pdf(request: PdfRequest):
    browser_action = BrowserActions()
    await browser_action.start()
    try:
        data = await browser_action.generate_pdf(url=request.url, format=request.format)
        return PdfResponse(data=data).dict()
    finally:
        await browser_action.close()

@app.post("/scrape")
@measure_time()
async def scrape_data(request: ScrapeRequests):
    browser_action = BrowserActions()
    await browser_action.start()
    try:
        data = await browser_action.scrape_data(
            url=request.url,
            locator=request.locator,
            user_agent=request.user_agent
        )
        return ScrapeResponse(data=data).dict()
    finally:
        await browser_action.close()

@app.get("/devices")
@measure_time()
async def get_devices():
    return DeviceListResponse(devices=device_list).dict()

@app.get("/browsers")
@measure_time()
async def get_browsers():
    return BrowserListResponse(browsers=browser_list).dict()
