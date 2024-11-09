from pydantic import BaseModel
from pydantic import HttpUrl, Field, field_validator
from typing import Optional, Literal

from constants import device_list, browser_list, pdf_format_list

class ScreenshotRequest(BaseModel):
    url: HttpUrl = Field(..., description="The URL of the website to take a screenshot of")
    # browser: Optional[Literal["chromium", "firefox", "webkit"]] = Field(None, description="The browser to use for the screenshot (e.g. 'chromium', 'firefox', 'webkit')", example="chromium")
    device: Optional[str] = Field(None, description="The device to use for the screenshot (e.g. 'iPhone 12 Pro Max', 'Samsung Galaxy S21')", example="desktop")
    full_page: Optional[bool] = Field(True, description="Whether to take a full-page screenshot", example=False)
    color_scheme: Optional[Literal["dark", "light"]] = Field("light", description="The color scheme to use for the screenshot (e.g. 'dark', 'light')", example="dark")
    locator: Optional[str] = Field(None, description="The locator to use for the screenshot (e.g. '#my-element')", example="#my-element")

class ScreenshotResponse(BaseModel):
    image_data: bytes

class PdfRequest(BaseModel):
    url: HttpUrl = Field(..., description="The URL of the website to generate a PDF of")
    format: Optional[str] = Field("A4", description="The format of the PDF (e.g. 'A4', 'Letter', 'Legal')", example="A4")

    @field_validator("format")
    def validate_format(cls, value):
        if value not in pdf_format_list:
            raise ValueError(f"Invalid format. Supported formats are {pdf_format_list}.")

class PdfResponse(BaseModel):
    pdf_data: bytes

class ScrapeRequests(BaseModel):
    url: HttpUrl = Field(..., description="The URL of the website to scrape")
    locator: Optional[str] = Field(None, description="The locator to use for the scraping (e.g. '#my-element')", example="#my-element")
    user_agent: Optional[str] = Field(None, description="The user agent to use for the scraping", example="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

class ScrapeResponse(BaseModel):
    data: bytes

class DeviceListResponse(BaseModel):
    devices: list[str]

class BrowserListResponse(BaseModel):
    browsers: list[str]

