from playwright.sync_api import sync_playwright
import os
from datetime import datetime
import asyncio
from urllib.parse import urlparse
import re

def sanitize_filename(url):
    """Convert URL to a valid filename"""
    parsed = urlparse(url)
    basename = parsed.netloc + parsed.path
    # Replace invalid filename characters
    basename = re.sub(r'[<>:"/\\|?*]', '_', basename)
    return basename[:150]  # Limit filename length

def take_screenshots(urls, output_dir="screenshots"):
    """
    Take full-page screenshots of multiple URLs
    
    Args:
        urls (list): List of URLs to screenshot
        output_dir (str): Directory to save screenshots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get current timestamp for the batch
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        
        # Create a new context with high viewport
        context = browser.new_context(
            viewport={'width': 1280, 'height': 1024}
        )
        
        # Create a new page
        page = context.new_page()
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"Processing {i}/{len(urls)}: {url}")
                
                # Navigate to the page
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Wait for any lazy-loaded content
                page.wait_for_timeout(2000)
                
                # Generate filename
                filename = f"{timestamp}_{sanitize_filename(url)}.png"
                filepath = os.path.join(output_dir, filename)
                
                # Take full page screenshot
                page.screenshot(path=filepath, full_page=True)
                
                print(f"Screenshot saved: {filepath}")
                
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                continue
        
        # Clean up
        browser.close()

def main():
    # Example URLs
    urls = [
        "https://www.fullstack.cafe/interview-questions/net-core",
        "https://www.fullstack.cafe/interview-questions/adonet",
        "https://www.fullstack.cafe/interview-questions/aspnet",
        "https://www.fullstack.cafe/interview-questions/aspnet-mvc",
        "https://www.fullstack.cafe/interview-questions/aspnet-web-api",
        "https://www.fullstack.cafe/interview-questions/agile-and-scrum"
    ]
    
    # Take screenshots
    take_screenshots(urls)

if __name__ == "__main__":
    main()