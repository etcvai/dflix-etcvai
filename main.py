import requests
import json
import sys

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
JSON_URL = "https://psplay.indevs.in/icctv"
OUTPUT_FILE = "icc.m3u8"

def generate_playlist():
    print(f"Fetching data from {JSON_URL}...")
    
    try:
        response = requests.get(JSON_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Network or JSON Error: {e}")
        sys.exit(1)

    # Start the M3U content
    m3u_content = ['#EXTM3U x-tvg-url=""']
    count = 0

    # ---------------------------------------------------------
    # PARSING LOGIC
    # ---------------------------------------------------------
    # The JSON structure is: root -> "tournaments" (list) -> "live_streams" (list)
    
    tournaments = data.get("tournaments", [])
    
    if not tournaments:
        print("No tournaments found in JSON.")
    
    for tourney in tournaments:
        # Get the list of streams for this tournament
        streams = tourney.get("live_streams", [])
        
        for stream in streams:
            # Extract basic info
            title = stream.get("title", "Unknown Match")
            mpd_url = stream.get("mpd")
            drm_keys = stream.get("keys")  # Format is usually "kid:key"
            
            # Extract Logo from the nested 'match' object
            match_info = stream.get("match", {})
            logo = match_info.get("thumbnail", "")

            # Only add if we have a valid link
            if mpd_url:
                # 1. INFO LINE
                m3u_content.append(f'#EXTINF:-1 tvg-id="{title}" tvg-name="{title}" tvg-logo="{logo}" group-title="ICC Live",{title}')
                
                # 2. KODI DRM PROPS (ClearKey)
                m3u_content.append('#KODIPROP:inputstream.adaptive.manifest_type=mpd')
                
                if drm_keys:
                    m3u_content.append('#KODIPROP:inputstream.adaptive.license_type=org.w3.clearkey')
                    # The JSON keys are already in "kid:key" format, which Kodi accepts directly
                    m3u_content.append(f'#KODIPROP:inputstream.adaptive.license_key={drm_keys}')
                
                # 3. STREAM URL
                m3u_content.append(mpd_url)
                count += 1

    # ---------------------------------------------------------
    # WRITE TO FILE
    # ---------------------------------------------------------
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(m3u_content))
        print(f"Success: Generated {OUTPUT_FILE} with {count} channels.")
    except Exception as e:
        print(f"File Write Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_playlist()
    
