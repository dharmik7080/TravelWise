import urllib.request
import re
import ssl

# Bypass SSL verification if needed
ssl._create_default_https_context = ssl._create_unverified_context

def test_unsplash(query):
    try:
        url = f"https://unsplash.com/s/photos/{urllib.parse.quote(query)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            # Look for image URLs in the HTML
            # Unsplash image URLs usually start with https://images.unsplash.com/photo-
            matches = re.findall(r'https://images\.unsplash\.com/photo-[^?"]+', html)
            if matches:
                # Deduplicate and filter out profile pictures or small icons
                unique_urls = list(set(matches))
                for img_url in unique_urls:
                    if 'profile' not in img_url and 'placeholder' not in img_url:
                        # Append parameters to crop/resize to 1200x800
                        full_url = f"{img_url}?auto=format&fit=crop&w=1200&h=800&q=80"
                        print(f"Found URL: {full_url}")
                        return full_url
        print("No image found for", query)
        return None
    except Exception as e:
        print(f"Error searching for {query}: {e}")
        return None

if __name__ == '__main__':
    url = test_unsplash("goa beach")
    if url:
        print("Successfully found image!")
        # Try downloading it
        try:
            urllib.request.urlretrieve(url, "goa_test.jpg")
            print("Successfully downloaded!")
        except Exception as e:
            print("Download failed:", e)
