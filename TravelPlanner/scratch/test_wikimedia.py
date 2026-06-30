import urllib.request
import urllib.parse
import json

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
        print("Search failed:", e)
        return None

if __name__ == '__main__':
    url = get_wikimedia_image("Srinagar Dal Lake")
    print("Found URL:", url)
