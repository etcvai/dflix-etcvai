import requests
import json
import os

# The Source URL
JSON_URL = "https://psplay.indevs.in/icctv"
OUTPUT_FILE = "icc.m3u8"

def generate_m3u8():
    try:
        print(f"Fetching data from {JSON_URL}...")
        response = requests.get(JSON_URL, timeout=15)
        response.raise_for_status()
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Error: content is not valid JSON")
            return

        # Handle different JSON structures (List vs Dictionary)
        # If the API returns {"channels": [...]}, change this to data.get("channels", [])
        items = data if isinstance(data, list) else data.values() if isinstance(data, dict) else []

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U x-tvg-url=\"\"\n")
            
            count = 0
            for item in items:
                # Attempt to find the correct keys for Name, URL, and Logo
                # You may need to adjust these keys based on the actual JSON output
                name = item.get("name") or item.get("title") or item.get("channel_name") or "Unknown Channel"
                link = item.get("url") or item.get("stream_url") or item.get("link") or item.get("stream")
                logo = item.get("logo") or item.get("icon") or item.get("image") or ""
                
                # Check for headers/user-agent requirements often needed for Kodi
                headers = item.get("headers", "")
                user_agent = item.get("user_agent", "")
                
                # Construct Kodi-specific License tags if DRM is present in JSON
                # Example: #KODIPROP:inputstream.adaptive.license_key=...
                
                if link:
                    # Append user-agent to link for Kodi if needed (pipe syntax)
                    if user_agent and "|" not in link:
                        link = f"{link}|User-Agent={user_agent}"
                    
                    f.write(f'#EXTINF:-1 tvg-id="{name}" tvg-name="{name}" tvg-logo="{logo}" group-title="ICC Live",{name}\n')
                    f.write(f"{link}\n")
                    count += 1
        
        print(f"Success: Generated {OUTPUT_FILE} with {count} channels.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    generate_m3u8()
