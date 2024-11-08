FROM python:3.11.10-slim

# Set the browser download path
ENV PLAYWRIGHT_BROWSERS_PATH=/browsers

# Install playwright and its dependencies
RUN pip install --upgrade playwright
RUN playwright install --with-deps firefox chromium webkit
 
# Set the permissions for the download path
RUN chmod -R 777 /browsers
