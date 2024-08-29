from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Function to run the Playwright script
def scrape_page(url):
    # Set up Playwright
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the URL
        page.goto(url)
        
        # Wait for the body tag to be present
        page.wait_for_selector('body')
        
        # Extract the HTML content
        html_content = page.content()
        
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Target only the body section of the webpage
        body = soup.body
        
        # Remove unwanted sections like <nav>, <header>, <footer>, <aside>, <script>, <style>, and elements used by screen readers
        for unwanted_tag in ['nav', 'header', 'footer', 'aside', 'script', 'style', 'meta', 'noscript']:
            for element in body.find_all(unwanted_tag):
                element.decompose()
        
        # Remove ARIA and other screen reader related elements
        for aria_attr in ['aria-hidden', 'role', 'aria-label', 'aria-labelledby', 'aria-describedby']:
            for element in body.find_all(attrs={aria_attr: True}):
                element.decompose()
        
        # Extract text from the specified tags within the body
        tags_to_extract = ['h2', 'h3', 'h4', 'h5', 'li', 'p']
        extracted_text = []
        for tag in tags_to_extract:
            for element in body.find_all(tag):
                extracted_text.append(element.get_text())
        
        # Combine all extracted text into one string (optional)
        # cleaned_text = "\n".join(extracted_text)
        
        # Print the cleaned text
        print(extracted_text)
        
        # Close the browser
        browser.close()

# URL of the webpage you want to scrape
url = 'https://rahma.health/en/family-planning/unplanned-pregnancy'
scrape_page(url)