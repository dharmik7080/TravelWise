from duckduckgo_search import DDGS
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def get_image(query):
    try:
        # Search unsplash.com via DDG
        search_query = f"site:images.unsplash.com {query}"
        print(f"Searching: {search_query}")
        with DDGS() as ddgs:
            results = ddgs.images(
                keywords=search_query,
                max_results=5
            )
            for r in results:
                img_url = r['image']
                # Clean up / resize Unsplash image if possible
                if 'images.unsplash.com' in img_url:
                    # Remove existing query params if any
                    base_url = img_url.split('?')[0]
                    # Format to 1200x800
                    formatted_url = f"{base_url}?auto=format&fit=crop&w=1200&h=800&q=80"
                    print(f"Found Unsplash image: {formatted_url}")
                    return formatted_url
                else:
                    print(f"Found other image: {img_url}")
                    return img_url
        return None
    except Exception as e:
        print("Search failed:", e)
        return None

if __name__ == '__main__':
    url = get_image("Goa Beach")
    if url:
        print("Url found, downloading...")
        try:
            urllib.request.urlretrieve(url, "goa_ddg.jpg")
            print("Downloaded successfully!")
        except Exception as e:
            print("Download failed:", e)
