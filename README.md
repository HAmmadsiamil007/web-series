# Movie Scraper

This Python script scrapes movie information (title, poster, and download link) from a specified website and saves the data to a JSON file. The script automatically handles pagination, follows redirects, and avoids duplicate entries.

## Features
- Extracts movie titles, posters, and download links.
- Handles pagination automatically.
- Avoids duplicate entries by checking existing data.
- Saves scraped data to a `movies.json` file.
- Configurable request headers and timeouts.

## Requirements
Make sure you have Python installed along with the required dependencies.

### Install Dependencies
Run the following command:
```sh
pip install requests beautifulsoup4
```

## How It Works
1. The script loads existing movie data from `movies.json`.
2. It scrapes movie listings from the specified website.
3. For each movie, it extracts details such as the title, poster, and download link.
4. The script avoids adding duplicate movies.
5. New data is appended to `movies.json`.

## Usage
Run the script with:
```sh
python scraper.py
```

## Configuration
Modify the `BASE_URL` variable in the script to set the target website:
```python
BASE_URL = "https://mms69.top/"  # Replace with actual site
```

### Adjustable Settings
You can tweak the following settings inside the script:
```python
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
REQUEST_TIMEOUT = 10  # Timeout for HTTP requests (in seconds)
SLEEP_BETWEEN_REQUESTS = 2  # Delay between requests to avoid bans
```

## Output
The scraped data is saved in `movies.json` in the following format:
```json
[
    {
        "title": "Movie Title",
        "poster": "https://example.com/image.jpg",
        "download_link": "https://example.com/download"
    }
]
```

## Error Handling
- If a movie page fails to load, the script prints an error and moves to the next movie.
- If pagination reaches a non-existent page, the script stops automatically.

## License
This project is for educational purposes only. Use responsibly.

