import asyncio
import os
import requests
from pyppeteer import launch
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from jerseys.models import Jersey

class Command(BaseCommand):
    help = 'Scrapes jerseys using Pyppeteer and stores them in the database'

    async def scrape_website(self):
        # Launch the browser with improved user agent and args
        browser = await launch({
            'executablePath': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            'headless': False,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--window-size=1280,720',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            ]
        })

        page = await browser.newPage()

        # Setting a user agent
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        # Start scraping from the main jersey page
        await page.goto('https://www.adidas.co.uk/men-football-jerseys', {'timeout': 30000, 'waitUntil': 'networkidle2'})
        self.stdout.write("Main page loaded successfully.")

        await page.waitForSelector('.product-card')
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Scrape individual jersey links
        jersey_links = []
        for jersey_data in soup.find_all('div', class_='product-card'):
            link_tag = jersey_data.find('a', class_='product-card__link')
            if link_tag:
                jersey_links.append(link_tag['href'])

        # Scrape data from each individual jersey page
        for jersey_url in jersey_links:
            await self.scrape_jersey_detail(page, jersey_url)

        await browser.close()

    async def scrape_jersey_detail(self, page, jersey_url):
        await page.goto(jersey_url, {'timeout': 30000, 'waitUntil': 'networkidle2'})
        self.stdout.write(f"Loading jersey details from {jersey_url}")

        await page.waitForSelector('.product-info')
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Extract jersey details
        name_tag = soup.find('h1', class_='product-title')
        price_tag = soup.find('span', class_='product-price')
        description_tag = soup.find('div', class_='product-description')
        image_tag = soup.find('img', class_='product-image')

        name = name_tag.text.strip() if name_tag else 'Unknown Name'
        price_text = price_tag.text.strip() if price_tag else 'Unknown Price'
        description = description_tag.text.strip() if description_tag else 'No Description Available'
        brand = 'Adidas'
        season = '2024'
        image_url = image_tag['src'] if image_tag else None

        # Logging for debugging
        self.stdout.write(f"Name: {name}, Price: {price_text}, Description: {description}")

        # Attempt to parse the price; handle potential errors
        try:
            price = float(price_text.replace('£', '').replace(',', '').strip()) if price_text != 'Unknown Price' else 0.0
        except ValueError as e:
            self.stderr.write(f"Error parsing price for {name}: {e}")
            price = 0.0  # Fallback value

        # Save or update the Jersey in the database
        jersey, created = Jersey.objects.update_or_create(
            name=name,
            defaults={
                'price': price,
                'description': description,
                'brand': brand,
                'season': season,
                'is_promoted': True
            }
        )

        # Save the image if a URL is available
        if image_url:
            image_path = os.path.join('media', 'jerseys', f"{jersey.id}.jpg")
            self.save_image_from_url(image_url, image_path)

    def handle(self, *args, **kwargs):
        asyncio.run(self.scrape_website())

    def save_image_from_url(self, url, file_path):
        try:
            response = requests.get(url)
            response.raise_for_status()
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as file:
                file.write(response.content)
                self.stdout.write("Image saved successfully.")
        except requests.exceptions.RequestException as e:
            self.stderr.write(f"Failed to save image from {url}. Error: {e}")
        except Exception as e:
            self.stderr.write(f"Error saving image: {e}")
