from fastapi import FastAPI, HTTPException
from models import *
from tools import measure_time
from BrowserActions import BrowserActions

app = FastAPI(docs_url="/")

@app.post("/screenshot")
@measure_time()
def take_screenshot(request: ScreenshotRequest):
    try:
        browser_action = BrowserActions(request.browser or "chromium")
        screenshot_data = browser_action.take_screenshot(
            url=request.url,
            device=request.device,
            color_scheme=request.color_scheme,
            full_page=request.full_page,
            locator=request.locator
        )
        return ScreenshotResponse(image_data=screenshot_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pdf")
@measure_time()
def generate_pdf(request: PdfRequest):
    try:
        browser_action = BrowserActions("chromium")
        pdf_data = browser_action.generate_pdf(url=request.url, format=request.format)
        return PdfResponse(pdf_data=pdf_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape")
@measure_time()
def scrape_data(request: ScrapeRequests):
    try:
        browser_action = BrowserActions("chromium")
        scraped_data = browser_action.scrape_data(
            url=request.url,
            locator=request.locator,
            user_agent=request.user_agent
        )
        return ScrapeResponse(data=scraped_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/devices")
@measure_time()
def get_devices():
    return DeviceListResponse(devices=device_list)

@app.get("/browsers")
@measure_time()
def get_browsers():
    return BrowserListResponse(browsers=browser_list)
