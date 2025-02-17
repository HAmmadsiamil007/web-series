import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin

# Configure settings
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
REQUEST_TIMEOUT = 10
SLEEP_BETWEEN_REQUESTS = 2

def load_existing_data():
    """Load existing data from movies.json file"""
    if os.path.exists('movies.json'):
        try:
            with open('movies.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_data(data):
    """Save data to movies.json file"""
    with open('movies.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_final_url(url):
    """Follow redirects to get final URL"""
    try:
        response = requests.head(
            url,
            headers=HEADERS,
            allow_redirects=True,
            timeout=REQUEST_TIMEOUT
        )
        return response.url
    except Exception as e:
        print(f"Error resolving URL {url}: {str(e)}")
        return url

def scrape_movie_page(movie_url):
    """Scrape individual movie page for details"""
    try:
        response = requests.get(
            movie_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"Failed to fetch movie page: {str(e)}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title_element = soup.find('h1', class_='entry-title')
    if not title_element:
        raise ValueError("Movie title not found")
    title = title_element.get_text(strip=True)

    # Extract poster image
    poster = None
    img = soup.find('img', class_='wp-post-image')
    if img and img.has_attr('src'):
        poster = img['src']

    # Extract download link
    download_link = None
    download_a = soup.find('a', string=lambda t: t and 'Click Here To Download' in t)
    if download_a and download_a.has_attr('href'):
        download_url = urljoin(movie_url, download_a['href'])
        download_link = get_final_url(download_url)

    return {
        'title': title,
        'poster': poster,
        'download_link': download_link
    }

def scrape_movies_on_page(soup, base_url):
    """Extract movie links from a listing page"""
    movie_links = []
    # Adjust selector based on actual website structure
    for link in soup.select('article a[href]'):
        href = link['href']
        full_url = urljoin(base_url, href)
        if full_url not in movie_links:
            movie_links.append(full_url)
    return movie_links

def scrape_site(base_url):
    """Main scraping function"""
    existing_data = load_existing_data()
    existing_titles = {m['title'] for m in existing_data}
    new_movies_added = 0

    page_num = 1
    while True:
        try:
            if page_num == 1:
                page_url = base_url
            else:
                page_url = urljoin(base_url, f'page/{page_num}/')

            print(f"Scraping page {page_num} ({page_url})...")
            
            response = requests.get(
                page_url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 404:
                print(f"Page {page_num} not found. Stopping pagination.")
                break

            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            movie_urls = scrape_movies_on_page(soup, base_url)
            print(f"Found {len(movie_urls)} movies on page {page_num}")

            for movie_url in movie_urls:
                try:
                    print(f"Processing movie: {movie_url}")
                    movie_data = scrape_movie_page(movie_url)
                    
                    if movie_data['title'] in existing_titles:
                        print(f"Duplicate found: {movie_data['title']}. Skipping.")
                        continue
                    
                    existing_data.append(movie_data)
                    existing_titles.add(movie_data['title'])
                    new_movies_added += 1
                    save_data(existing_data)
                    print(f"Added new movie: {movie_data['title']}")

                except Exception as e:
                    print(f"Error processing {movie_url}: {str(e)}")
                
                time.sleep(SLEEP_BETWEEN_REQUESTS)

            page_num += 1
            time.sleep(SLEEP_BETWEEN_REQUESTS)

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error on page {page_num}: {str(e)}")
            break
        except Exception as e:
            print(f"Error processing page {page_num}: {str(e)}")
            break

    print(f"Scraping complete. Added {new_movies_added} new movies.")

if __name__ == "__main__":
    BASE_URL = "https://mms69.top/"  # Replace this with the actual base URL
    scrape_site(BASE_URL)
