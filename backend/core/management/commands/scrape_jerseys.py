import uuid
import asyncio
import os
import django
import requests
import random
import re
from datetime import datetime
from decimal import Decimal
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async
from playwright.async_api import async_playwright
from django.core.management.base import BaseCommand
from core.models import Jersey

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

class Command(BaseCommand):
    help = 'Scrapes jersey details from the Nike website.'

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36'
    ]

    IMAGE_DIR = 'media/jerseys/'  # Directory to save images

    def normalize_team_name(self, team):
        team = team.replace('.', '').strip()
        normalization_map = {
            'Chelsea FC': 'Chelsea F.C.',
            'Chelsea F.C': 'Chelsea F.C.',
            'Chelsea F.C.': 'Chelsea F.C.',
            'Liverpool FC': 'Liverpool F.C.',
            'Liverpool F.C': 'Liverpool F.C.',
            'Liverpool F.C.': 'Liverpool F.C.',
            'Barcelona': 'FC Barcelona',
            'FC Barcelona': 'FC Barcelona',
        }
        return normalization_map.get(team, team)

    async def scrape_jersey_detail(self, context, jersey_url):
        page = await context.new_page()
        try:
            self.stdout.write(f"Loading jersey details from {jersey_url}")
            response = await page.goto(jersey_url, timeout=120000)

            if response.status != 200:
                self.stderr.write(f"Failed to load details for {jersey_url}: Status code {response.status}")
                return

            await page.wait_for_load_state('networkidle', timeout=120000)
            await page.wait_for_timeout(random.uniform(2000, 5000))

            content = await page.content()
            if not self.is_valid_jersey_page(content):
                self.stderr.write(f"Failed to load valid details for {jersey_url}: Invalid page content.")
                return

            soup = BeautifulSoup(content, 'html.parser')
            name, price_text, description, color, brand, team, sizes = self.extract_jersey_details_from_soup(soup)

            price = self.parse_price(price_text)
            image_urls = self.extract_image_urls(soup)
            saved_image_paths = await self.save_images(image_urls, name)

            self.stdout.write(f"Extracted values - Name: {name}, Price: {price}, Description: {description}, Color: {color}, Brand: {brand}, Team: {team}, Sizes: {sizes}, Images: {saved_image_paths}")

            normalized_team = self.normalize_team_name(team)
            await self.save_or_update_jersey(brand, normalized_team, price, description, color, saved_image_paths, sizes)

        except Exception as e:
            self.stderr.write(f"Error scraping {jersey_url}: {e}")
        finally:
            await page.close()

    async def scrape_website(self):
        async with async_playwright() as p:
            user_agent = random.choice(self.USER_AGENTS)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(user_agent=user_agent)

            headers = {
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.nike.com/gb/',
            }

            page = await context.new_page()
            await page.set_extra_http_headers(headers)

            main_url = "https://www.nike.com/gb/w/mens-kits-jerseys-3a41eznik1"
            self.stdout.write(f"Loading main page: {main_url}")
            response = await page.goto(main_url)

            if response.status != 200:
                self.stderr.write(f"Failed to load main page: {response.status}")
                return

            await page.wait_for_load_state('networkidle')

            product_links = await page.query_selector_all('a[href*="/t/"]')
            jersey_links = [await link.get_attribute('href') for link in product_links]
            self.stdout.write(f"Found {len(jersey_links)} jersey links.")

            for jersey_url in jersey_links:
                await self.scrape_jersey_detail(context, jersey_url)

            await context.close()
            await browser.close()

    def is_valid_jersey_page(self, content):
        return 'Product not found' not in content and 'jersey' in content.lower()

    def extract_jersey_details_from_soup(self, soup):
        name = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'N/A'
        price_tag = soup.find('div', id='price-container')
        price_text = price_tag.get_text(strip=True) if price_tag else 'N/A'
        color_tag = soup.find('li', {'data-testid': 'product-description-color-description'})
        color = color_tag.get_text(strip=True).replace('Colour Shown:', '') if color_tag else 'N/A'
        description_tag = soup.find('p', {'data-testid': 'product-description'})
        description = description_tag.get_text(strip=True) if description_tag else 'N/A'
        sizes = self.extract_sizes_from_soup(soup)
        
        brand = "Nike"
        team = self.extract_team_from_name(name)

        return name, price_text, description, color, brand, team, sizes

    def extract_sizes_from_soup(self, soup):
        size_options = []
        size_labels = soup.select('div[data-testid="pdp-grid-selector-grid"] label')

        for label in size_labels:
            size_options.append(label.get_text(strip=True)) 
        
        return ', '.join(size_options) if size_options else 'N/A'

    def extract_team_from_name(self, name):
        team_mapping = {
            'Barcelona': 'F.C. Barcelona',
            'PSG': 'Paris Saint-Germain',
            'Liverpool': 'Liverpool F.C.',
            'Chelsea': 'Chelsea F.C.',
            'Tottenham': 'Tottenham Hotspur',
            'Inter Milan': 'Inter Milan',
            'Atlético': 'Atlético Madrid',
            'Hertha Berlin': 'Hertha Berlin',
            'Wolfsburg': 'VfL Wolfsburg',
            'Pumas': 'UNAM Pumas',
            'Club América': 'Club América',
            'Corinthians': 'Sport Club Corinthians Paulista',
            'Brazil': 'Brazil National Team',
            'England': 'England National Team',
            'France': 'France National Team',
            'Poland': 'Poland National Team',
            'Norway': 'Norway National Team',
        }
        
        for key, value in team_mapping.items():
            if key in name:
                return value

        return 'N/A'

    def extract_country_from_description(self, description):
        country_mapping = {
            'England': ['Chelsea', 'Tottenham', 'Liverpool', 'England'],
            'France': ['PSG', 'France'],
            'Brazil': ['Brazil', 'Corinthians'],
            'Italy': ['Inter Milan'],
            'Spain': ['Atlético Madrid', 'F.C. Barcelona'],
            'Mexico': ['Club América', 'Pumas'],
            'Germany': ['Hertha Berlin', 'Wolfsburg'],
            'Poland': ['Poland'],
            'Norway': ['Norway']
        }
        
        for country, teams in country_mapping.items():
            if any(team in description for team in teams):
                return country

        return 'N/A'

    def parse_price(self, price_text):
        match = re.search(r'\d+(\.\d{1,2})?', price_text)
        if match:
            try:
                return Decimal(match.group(0))
            except ValueError:
                self.stderr.write(f"Error converting price: {match.group(0)}")
        return Decimal('0.00')

    def get_release_date(self, description):
        date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', description)  # Format: MM/DD/YYYY
        if date_match:
            return datetime.strptime(date_match.group(0), '%d/%m/%Y')
        return None

    async def save_or_update_jersey(self, brand, team, price, description, color, image_paths, sizes, season='2024'):
        current_date = datetime.now()
        release_date = self.get_release_date(description)

        # Determine the flags for promotions and new releases
        is_new_release = False
        is_upcoming = False
        is_promoted = False

        if release_date:
            if (current_date - release_date).days < 30:
                is_new_release = True
            if release_date > current_date:
                is_upcoming = True

        if "limited edition" in description.lower():
            is_promoted = True

        # Use get_or_create to find or create the jersey
        jersey, created = await sync_to_async(Jersey.objects.get_or_create)(
            brand=brand,
            team=team,
            defaults={
                'price': price,
                'description': description,
                'color': color,
                'sizes': sizes,
                'is_new_release': is_new_release,
                'is_upcoming': is_upcoming,
                'is_promoted': is_promoted,
                'season': season,
            }
        )

        if not created:
            # Check if values have changed before updating
            if jersey.price != price:
                jersey.price = price

            if jersey.sizes != sizes:
                jersey.sizes = sizes

            if jersey.is_new_release != is_new_release:
                jersey.is_new_release = is_new_release
            if jersey.is_upcoming != is_upcoming:
                jersey.is_upcoming = is_upcoming
            if jersey.is_promoted != is_promoted:
                jersey.is_promoted = is_promoted

            if not jersey.image_path and image_paths:
                jersey.image_path = image_paths[0] if image_paths else None

            # Save changes only if any field was updated
            if (
                jersey.price != price or 
                jersey.sizes != sizes or 
                jersey.is_new_release != is_new_release or 
                jersey.is_upcoming != is_upcoming or 
                jersey.is_promoted != is_promoted
            ):
                await sync_to_async(jersey.save)()

    async def save_images(self, image_urls, name):
        saved_image_paths = []
        for url in image_urls:
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    cleaned_name = re.sub(r'[<>:"/\\|?*]', '_', name)  # Sanitize the name
                    filename = f"{cleaned_name}_{uuid.uuid4()}.jpg"  # Use UUID for uniqueness
                    file_path = os.path.join(self.IMAGE_DIR, filename)

                    # Make sure the directory exists
                    os.makedirs(self.IMAGE_DIR, exist_ok=True)

                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    saved_image_paths.append(file_path)
                    self.stdout.write(f"Image saved to: {file_path}")  # Log the saved path
                else:
                    self.stderr.write(f"Failed to download image {url}: {response.status_code}")
            except Exception as e:
                self.stderr.write(f"Error saving image {url}: {e}")
        return saved_image_paths

    def extract_image_urls(self, soup):
        image_tags = soup.find_all('img')
        return [img['src'] for img in image_tags if img.get('src')]

    def handle(self, *args, **kwargs):
        asyncio.run(self.scrape_website())
import uuid
import asyncio
import os
import django
import requests
import random
import re
from datetime import datetime
from decimal import Decimal
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async
from playwright.async_api import async_playwright
from django.core.management.base import BaseCommand
from core.models import Jersey

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

class Command(BaseCommand):
    help = 'Scrapes jersey details from the Nike website.'

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36'
    ]

    IMAGE_DIR = 'media/jerseys/'  # Directory to save images

    def normalize_team_name(self, team):
        team = team.replace('.', '').strip()
        normalization_map = {
            'Chelsea FC': 'Chelsea F.C.',
            'Chelsea F.C': 'Chelsea F.C.',
            'Chelsea F.C.': 'Chelsea F.C.',
            'Liverpool FC': 'Liverpool F.C.',
            'Liverpool F.C': 'Liverpool F.C.',
            'Liverpool F.C.': 'Liverpool F.C.',
            'Barcelona': 'FC Barcelona',
            'FC Barcelona': 'FC Barcelona',
        }
        return normalization_map.get(team, team)

    async def scrape_jersey_detail(self, context, jersey_url):
        page = await context.new_page()
        try:
            self.stdout.write(f"Loading jersey details from {jersey_url}")
            response = await page.goto(jersey_url, timeout=120000)

            if response.status != 200:
                self.stderr.write(f"Failed to load details for {jersey_url}: Status code {response.status}")
                return

            await page.wait_for_load_state('networkidle', timeout=120000)
            await page.wait_for_timeout(random.uniform(2000, 5000))

            content = await page.content()
            if not self.is_valid_jersey_page(content):
                self.stderr.write(f"Failed to load valid details for {jersey_url}: Invalid page content.")
                return

            soup = BeautifulSoup(content, 'html.parser')
            name, price_text, description, color, brand, team, sizes = self.extract_jersey_details_from_soup(soup)

            price = self.parse_price(price_text)
            image_urls = self.extract_image_urls(soup)
            saved_image_paths = await self.save_images(image_urls, name)

            self.stdout.write(f"Extracted values - Name: {name}, Price: {price}, Description: {description}, Color: {color}, Brand: {brand}, Team: {team}, Sizes: {sizes}, Images: {saved_image_paths}")

            normalized_team = self.normalize_team_name(team)
            await self.save_or_update_jersey(brand, normalized_team, price, description, color, saved_image_paths, sizes)

        except Exception as e:
            self.stderr.write(f"Error scraping {jersey_url}: {e}")
        finally:
            await page.close()

    async def scrape_website(self):
        async with async_playwright() as p:
            user_agent = random.choice(self.USER_AGENTS)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(user_agent=user_agent)

            headers = {
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.nike.com/gb/',
            }

            page = await context.new_page()
            await page.set_extra_http_headers(headers)

            main_url = "https://www.nike.com/gb/w/mens-kits-jerseys-3a41eznik1"
            self.stdout.write(f"Loading main page: {main_url}")
            response = await page.goto(main_url)

            if response.status != 200:
                self.stderr.write(f"Failed to load main page: {response.status}")
                return

            await page.wait_for_load_state('networkidle')

            product_links = await page.query_selector_all('a[href*="/t/"]')
            jersey_links = [await link.get_attribute('href') for link in product_links]
            self.stdout.write(f"Found {len(jersey_links)} jersey links.")

            for jersey_url in jersey_links:
                await self.scrape_jersey_detail(context, jersey_url)

            await context.close()
            await browser.close()

    def is_valid_jersey_page(self, content):
        return 'Product not found' not in content and 'jersey' in content.lower()

    def extract_jersey_details_from_soup(self, soup):
        name = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'N/A'
        price_tag = soup.find('div', id='price-container')
        price_text = price_tag.get_text(strip=True) if price_tag else 'N/A'
        color_tag = soup.find('li', {'data-testid': 'product-description-color-description'})
        color = color_tag.get_text(strip=True).replace('Colour Shown:', '') if color_tag else 'N/A'
        description_tag = soup.find('p', {'data-testid': 'product-description'})
        description = description_tag.get_text(strip=True) if description_tag else 'N/A'
        sizes = self.extract_sizes_from_soup(soup)
        
        brand = "Nike"
        team = self.extract_team_from_name(name)

        return name, price_text, description, color, brand, team, sizes

    def extract_sizes_from_soup(self, soup):
        size_options = []
        size_labels = soup.select('div[data-testid="pdp-grid-selector-grid"] label')

        for label in size_labels:
            size_options.append(label.get_text(strip=True)) 
        
        return ', '.join(size_options) if size_options else 'N/A'

    def extract_team_from_name(self, name):
        team_mapping = {
            'Barcelona': 'F.C. Barcelona',
            'PSG': 'Paris Saint-Germain',
            'Liverpool': 'Liverpool F.C.',
            'Chelsea': 'Chelsea F.C.',
            'Tottenham': 'Tottenham Hotspur',
            'Inter Milan': 'Inter Milan',
            'Atlético': 'Atlético Madrid',
            'Hertha Berlin': 'Hertha Berlin',
            'Wolfsburg': 'VfL Wolfsburg',
            'Pumas': 'UNAM Pumas',
            'Club América': 'Club América',
            'Corinthians': 'Sport Club Corinthians Paulista',
            'Brazil': 'Brazil National Team',
            'England': 'England National Team',
            'France': 'France National Team',
            'Poland': 'Poland National Team',
            'Norway': 'Norway National Team',
        }
        
        for key, value in team_mapping.items():
            if key in name:
                return value

        return 'N/A'

    def extract_country_from_description(self, description):
        country_mapping = {
            'England': ['Chelsea', 'Tottenham', 'Liverpool', 'England'],
            'France': ['PSG', 'France'],
            'Brazil': ['Brazil', 'Corinthians'],
            'Italy': ['Inter Milan'],
            'Spain': ['Atlético Madrid', 'F.C. Barcelona'],
            'Mexico': ['Club América', 'Pumas'],
            'Germany': ['Hertha Berlin', 'Wolfsburg'],
            'Poland': ['Poland'],
            'Norway': ['Norway']
        }
        
        for country, teams in country_mapping.items():
            if any(team in description for team in teams):
                return country

        return 'N/A'

    def parse_price(self, price_text):
        match = re.search(r'\d+(\.\d{1,2})?', price_text)
        if match:
            try:
                return Decimal(match.group(0))
            except ValueError:
                self.stderr.write(f"Error converting price: {match.group(0)}")
        return Decimal('0.00')

    def get_release_date(self, description):
        date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', description)  # Format: MM/DD/YYYY
        if date_match:
            return datetime.strptime(date_match.group(0), '%d/%m/%Y')
        return None

    async def save_or_update_jersey(self, brand, team, price, description, color, image_paths, sizes, season='2024'):
        current_date = datetime.now()
        release_date = self.get_release_date(description)

        # Determine the flags for promotions and new releases
        is_new_release = False
        is_upcoming = False
        is_promoted = False

        if release_date:
            if (current_date - release_date).days < 30:
                is_new_release = True
            if release_date > current_date:
                is_upcoming = True

        if "limited edition" in description.lower():
            is_promoted = True

        # Async DB save
        jersey, created = await sync_to_async(Jersey.objects.get_or_create)(
            brand=brand,
            team=team,
            price=price,
            defaults={
                'season': season,
                'description': description,
                'color': color,
                'images': image_paths,
                'sizes': sizes,
                'is_new_release': is_new_release,
                'is_promoted': is_promoted,
                'is_upcoming': is_upcoming
            }
        )

        if not created:
            jersey.price = price
            jersey.description = description
            jersey.color = color
            jersey.images = image_paths
            jersey.sizes = sizes
            jersey.is_new_release = is_new_release
            jersey.is_promoted = is_promoted
            jersey.is_upcoming = is_upcoming
            await sync_to_async(jersey.save)()

    def download_image(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception as e:
            self.stderr.write(f"Failed to download image: {url} - {e}")
            return None

    async def save_images(self, image_urls, jersey_name):
        saved_paths = []
        for idx, url in enumerate(image_urls):
            image_data = self.download_image(url)
            if image_data:
                unique_filename = f"{uuid.uuid4()}_{idx}.jpg"
                save_path = os.path.join(self.IMAGE_DIR, unique_filename)
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                saved_paths.append(save_path)
        return saved_paths

    def extract_image_urls(self, soup):
        image_tags = soup.find_all('img', {'src': re.compile(r'https://.*\.jpg')})
        image_urls = [tag['src'] for tag in image_tags]
        return image_urls

    def handle(self, *args, **kwargs):
        asyncio.run(self.scrape_website())
