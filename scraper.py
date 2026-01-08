import requests
from bs4 import BeautifulSoup
import time

# Configuration
BASE_URL = "https://dflix.discoveryftp.net"
OUTPUT_FILE = "dflix_playlist.m3u"
# [span_5](start_span)Categories from your Kotlin code[span_5](end_span)
CATEGORIES = [
    ("Bangla", "category/Bangla"),
    ("English", "category/English"),
    ("Hindi", "category/Hindi"),
    ("Tamil", "category/Tamil"),
    ("Animation", "category/Animation")
]

def get_session():
    [span_6](start_span)"""Mimics the login() function from Kotlin[span_6](end_span)."""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    try:
        # [span_7](start_span)The provider uses /login/demo to get cookies[span_7](end_span)
        print("Logging in...")
        session.get(f"{BASE_URL}/login/demo", timeout=15)
        return session
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def scrape_movies(session):
    playlist_entries = []
    
    for name, route in CATEGORIES:
        print(f"Scraping Category: {name}")
        # Scrape page 1 of each category to keep it fast
        # [span_8](start_span)Corresponds to getMainPage in Kotlin[span_8](end_span)
        list_url = f"{BASE_URL}/m/{route}/1" 
        
        try:
            resp = session.get(list_url, timeout=10)
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # [span_9](start_span)Select movie cards[span_9](end_span)
            cards = soup.select("div.card")
            
            for card in cards:
                try:
                    # [span_10](start_span)Logic from toResult()[span_10](end_span)
                    link_tag = card.select_one("div.card > a:nth-child(1)")
                    title_tag = card.select_one("div.card > div:nth-child(2) > h3:nth-child(1)")
                    img_tag = card.select_one("div.poster > img:nth-child(1)")
                    
                    if link_tag and title_tag:
                        details_url = BASE_URL + link_tag['href']
                        title = title_tag.get_text(strip=True)
                        poster = img_tag['src'] if img_tag else ""
                        
                        # [span_11](start_span)Go to details page to get the actual video link[span_11](end_span)
                        # [span_12](start_span)Logic from load()[span_12](end_span)
                        details_resp = session.get(details_url, timeout=10)
                        details_soup = BeautifulSoup(details_resp.content, 'html.parser')
                        
                        # [span_13](start_span)Extract the 'dataUrl' which is the video link[span_13](end_span)
                        video_btn = details_soup.select_one("div.col-md-12:nth-child(3) > div:nth-child(1) > a:nth-child(1)")
                        
                        if video_btn:
                            stream_url = video_btn['href']
                            
                            # Create M3U Entry
                            entry = f'#EXTINF:-1 tvg-logo="{poster}" group-title="{name}",{title}\n{stream_url}'
                            playlist_entries.append(entry)
                            print(f"  Found: {title}")
                except Exception as e:
                    print(f"  Error parsing card: {e}")
                    continue
                    
        except Exception as e:
            print(f"Failed to scrape category {name}: {e}")
            
    return playlist_entries

def main():
    session = get_session()
    if not session:
        return

    print("Starting scrape...")
    entries = scrape_movies(session)
    
    # Write to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("\n".join(entries))
    
    print(f"Done! Saved {len(entries)} items to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
  
