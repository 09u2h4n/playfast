from fastapi import FastAPI, HTTPException, Response, status
from models import *
from tools import measure_time, dummy_function
from BrowserActions import BrowserActions

app = FastAPI(
    title="SwarmUI Browser Automation API",
    description="API for browser automation tasks including screenshots, PDF generation, and web scraping",
    version="1.0.0",
    docs_url="/"
)

browser_actions = BrowserActions()

@app.get("/health", tags=["System"])
def health():
    """Check if the API is running."""
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/screenshot", 
         response_model=ScreenshotResponse,
         tags=["Browser Actions"])
@measure_time()
def screenshot(request: ScreenshotRequest):
    """Take a screenshot of the specified webpage."""
    try:
        data = browser_actions.take_screenshot(data=request)
        return ScreenshotResponse(image_data=data).dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/pdf",
         response_model=PdfResponse,
         tags=["Browser Actions"])
@measure_time()
def pdf(request: PdfRequest):
    """Generate a PDF of the specified webpage."""
    try:
        data = browser_actions.generate_pdf(data=request)
        return PdfResponse(pdf_data=data).dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/scrape",
         response_model=ScrapeResponse,
         tags=["Browser Actions"])
@measure_time()
def scrape(request: ScrapeRequest):
    """Scrape content from the specified webpage."""
    try:
        data = browser_actions.scrape_content(data=request)
        return ScrapeResponse(data=data).dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/devices",
        response_model=DeviceListResponse,
        tags=["Configuration"])
@measure_time()
def devices():
    """Get list of available device configurations."""
    try:
        return DeviceListResponse(devices=device_list).dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/browsers",
        response_model=BrowserListResponse,
        tags=["Configuration"])
@measure_time()
def browsers():
    """Get list of available browser configurations."""
    try:
        return BrowserListResponse(browsers=browser_list).dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
