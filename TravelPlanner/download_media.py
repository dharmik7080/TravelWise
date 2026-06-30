import os
import urllib.request
import urllib.parse
import json
import io
import shutil
from PIL import Image

# Setup Django environment
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TravelPlanner.settings')
django.setup()

from destinations.models import Destination
from attractions.models import Attraction
from packages.models import Package

# Fallback high-quality images for categories
FALLBACK_IMAGES = {
    "beach": "https://upload.wikimedia.org/wikipedia/commons/d/dd/Calangute_Beach_Goa.jpg",
    "hill_station": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Shimla_hills.jpg",
    "heritage": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Amer_Fort_Jaipur.jpg",
    "wildlife": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Bengal_Tiger_in_Ranthambhore.jpg",
    "adventure": "https://upload.wikimedia.org/wikipedia/commons/8/87/Trekking_in_Himalayas.jpg",
    "spiritual": "https://upload.wikimedia.org/wikipedia/commons/0/02/Ganga_Aarti_Varanasi.jpg",
    "city": "https://upload.wikimedia.org/wikipedia/commons/0/09/Gateway_of_India_Mumbai.jpg",
    "nature": "https://upload.wikimedia.org/wikipedia/commons/7/75/Munnar_tea_gardens.jpg"
}

def get_wikimedia_image(query):
    try:
        url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"file:{query}",
            "gsrlimit": 3,
            "prop": "imageinfo",
            "iiprop": "url",
            "origin": "*"
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        headers = {'User-Agent': 'TravelWise/1.0 (contact@travelwise.com)'}
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode('utf-8'))
            pages = res.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if "imageinfo" in page_info:
                    img_url = page_info["imageinfo"][0]["url"]
                    if img_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                        return img_url
        return None
    except Exception as e:
        print(f"Wikimedia search failed for '{query}': {e}")
        return None

def save_and_optimize_image(raw_data, filepath):
    try:
        image = Image.open(io.BytesIO(raw_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        width, height = image.size
        target_ratio = 3 / 2
        current_ratio = width / height
        
        if current_ratio > target_ratio:
            new_width = int(target_ratio * height)
            offset = (width - new_width) // 2
            image = image.crop((offset, 0, offset + new_width, height))
        else:
            new_height = int(width / target_ratio)
            offset = (height - new_height) // 2
            image = image.crop((0, offset, width, offset + new_height))
            
        image = image.resize((1200, 800), Image.Resampling.LANCZOS)
        
        # Ensure parent directories exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        image.save(filepath, "JPEG", quality=85, optimize=True)
        print(f"Saved optimized image to {filepath}")
        return True
    except Exception as e:
        print(f"Failed to process and save image to {filepath}: {e}")
        return False

def download_and_process_url(url, filepath):
    try:
        headers = {'User-Agent': 'TravelWise/1.0 (contact@travelwise.com)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_data = response.read()
            return save_and_optimize_image(raw_data, filepath)
    except Exception as e:
        print(f"Failed to download image from {url}: {e}")
        return False

def main():
    print("Creating media subdirectories...")
    os.makedirs("media/destinations", exist_ok=True)
    os.makedirs("media/attractions", exist_ok=True)
    os.makedirs("media/packages", exist_ok=True)

    # 1. Download Destination Images
    destinations = Destination.objects.all()
    print(f"Processing {destinations.count()} destinations...")
    for idx, dest in enumerate(destinations, 1):
        slug = dest.destination_name.lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('-', '_')
        filepath = f"media/destinations/{slug}.jpg"
        
        # Skip if already exists
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            print(f"[{idx}/75] Destination image for '{dest.destination_name}' already exists. Skipping.")
            dest.image = f"destinations/{slug}.jpg"
            dest.save()
            continue

        print(f"[{idx}/75] Searching image for '{dest.destination_name}' ({dest.category})...")
        img_url = get_wikimedia_image(dest.destination_name)
        if not img_url:
            # Try searching with city or state
            img_url = get_wikimedia_image(f"{dest.destination_name} {dest.state}")
            
        if not img_url:
            # Fallback to category standard image
            cat_key = dest.category.lower().replace(' ', '_')
            img_url = FALLBACK_IMAGES.get(cat_key, FALLBACK_IMAGES["nature"])
            print(f"Using category fallback for '{dest.destination_name}': {cat_key}")

        success = download_and_process_url(img_url, filepath)
        if success:
            dest.image = f"destinations/{slug}.jpg"
            dest.save()

    # 2. Download Attraction Images (Search specific or reuse destination)
    attractions = Attraction.objects.all()
    print(f"Processing {attractions.count()} attractions...")
    for idx, attr in enumerate(attractions, 1):
        slug = attr.attraction_name.lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('-', '_')
        filepath = f"media/attractions/{slug}.jpg"
        
        # Reusing the destination image (copy file to attractions folder to keep unique paths)
        dest_slug = attr.destination.destination_name.lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('-', '_')
        dest_filepath = f"media/destinations/{dest_slug}.jpg"
        if os.path.exists(dest_filepath):
            shutil.copy(dest_filepath, filepath)
            attr.image = f"attractions/{slug}.jpg"
        else:
            attr.image = attr.destination.image.name
        attr.save()

    # 3. Copy Package Images (Reuse corresponding destination image)
    packages = Package.objects.all()
    print(f"Processing {packages.count()} packages...")
    for idx, pkg in enumerate(packages, 1):
        dest_slug = pkg.destination.destination_name.lower().replace(' ', '_').replace('&', 'and').replace('/', '_').replace('-', '_')
        pkg_type_slug = pkg.package_type.lower()
        filepath = f"media/packages/{dest_slug}-{pkg_type_slug}.jpg"

        dest_filepath = f"media/destinations/{dest_slug}.jpg"
        if os.path.exists(dest_filepath):
            shutil.copy(dest_filepath, filepath)
            pkg.image = f"packages/{dest_slug}-{pkg_type_slug}.jpg"
        else:
            pkg.image = pkg.destination.image.name
        pkg.save()

    print("Media population and database mapping completed successfully!")

if __name__ == '__main__':
    main()
