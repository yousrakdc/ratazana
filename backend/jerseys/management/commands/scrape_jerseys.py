import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from jerseys.models import Jersey

class Command(BaseCommand):
    help = 'Scrapes jerseys using Pyppeteer and stores them in the database'

    async def scrape_website(self):
        # Launch headless browser
        browser = await launch(
            headless=True,
            executablePath='/usr/bin/chromium',
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )

        page = await browser.newPage()

        # Go to the target URL
        await page.goto('https://www.adidas.co.uk/men-football-jerseys')

        # Wait for the page to load
        await page.waitForSelector('.product-card')

        # Get page content
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Scrape data
        for jersey_data in soup.find_all('div', class_='product-card'):
            name_tag = jersey_data.find('h3', class_='product-card__title')
            price_tag = jersey_data.find('span', class_='product-card__price')
            team_tag = jersey_data.find('div', class_='product-card__team')

            name = name_tag.text.strip() if name_tag else 'Unknown Name'
            price_text = price_tag.text.strip() if price_tag else 'Unknown Price'
            team = team_tag.text.strip() if team_tag else 'Unknown Team'
            brand = 'Adidas'
            season = '2024'

            print(f"Name: {name}, Price: {price_text}, Team: {team}, Brand: {brand}, Season: {season}")

            # Save or update the Jersey in the database
            Jersey.objects.update_or_create(
                name=name,
                defaults={
                    'price': float(price_text.replace('£', '').replace(',', '').strip()) if price_text != 'Unknown Price' else 0.0,
                    'team': team,
                    'brand': brand,
                    'season': season,
                    'is_promoted': True
                }
            )

        # Close browser
        await browser.close()

    def handle(self, *args, **kwargs):
        asyncio.get_event_loop().run_until_complete(self.scrape_website())

