from fastapi import FastAPI
from models import *
from tools import dummy_function, measure_time
from BrowserActions import BrowserActions

app = FastAPI(docs_url="/")

@app.post("/screenshot")
@measure_time()
def take_screenshot(request: ScreenshotRequest):
    browser_action = BrowserActions(browser=request.browser)
    return ScreenshotResponse(data=browser_action.take_screenshot(url=request.url, device=request.device, color_scheme=request.color_scheme, full_page=request.full_page, locator=request.locator)).dict()

@app.post("/pdf")
@measure_time()
def generate_pdf(request: PdfRequest):
    browser_action = BrowserActions()
    return PdfResponse(data=browser_action.generate_pdf(url=request.url, format=request.url)).dict()

@app.post("/scrape")
@measure_time()
def scrape_data(request: ScrapeRequests):
    browser_action = BrowserActions()
    return ScrapeResponse(data=browser_action.scrape_data(url=request.url, locator=request.locator, user_agent=request.user_agent)).dict()

@app.get("/devices")
@measure_time()
def get_devices():
    return DeviceListResponse(devices=device_list).dict()

@app.get("/browsers")
@measure_time()
def get_browsers():
    return BrowserListResponse(browsers=browser_list).dict()

