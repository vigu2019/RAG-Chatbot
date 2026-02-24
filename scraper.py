import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def scrape_website(url, max_pages=5, max_page_size=2_000_000):

    visited = set()
    to_visit = [url]
    all_text = []
    sources = []

    base_domain = urlparse(url).netloc

    headers = {
        "User-Agent": "Mozilla/5.0 (HackathonBot)"
    }

    while to_visit and len(visited) < max_pages:

        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        try:
            response = requests.get(current_url, headers=headers, timeout=5)

            # Skip bad status codes
            if response.status_code != 200:
                continue

            # Skip non-HTML content
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue

            # Skip extremely large pages
            if len(response.content) > max_page_size:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove noisy elements
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside"]):
                tag.decompose()

            text = soup.get_text(separator=" ")
            text = re.sub(r"\s+", " ", text).strip()

            # Avoid empty or extremely short pages
            if len(text) > 300:
                all_text.append(text)
                sources.append(current_url)

            visited.add(current_url)

            # Extract internal links safely
            for link in soup.find_all("a", href=True):

                full_url = urljoin(current_url, link["href"])
                parsed = urlparse(full_url)

                # Clean URL (remove query & fragment)
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

                # Skip external domains
                if parsed.netloc != base_domain:
                    continue

                # Skip unwanted paths (optional filtering)
                if any(x in clean_url.lower() for x in ["login", "signup", "register", "privacy", "terms"]):
                    continue

                if clean_url not in visited and clean_url not in to_visit:
                    to_visit.append(clean_url)

        except Exception:
            continue

    combined_text = " ".join(all_text)

    return {
        "text": combined_text,
        "sources": sources,
        "pages_scraped": len(sources),
        "total_characters": len(combined_text)
    }