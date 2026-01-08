import requests
import os

# 1. The exact URL from your JSON
url = "https://akashgo.noobmaster.xyz/?api=iptv_m3u"

# 2. ALL Headers exactly as they appear in your request.json
headers = {
    "Host": "akashgo.noobmaster.xyz",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.12.0"
}

def fetch_playlist():
    try:
        print("1. Sending request to server...")
        # We use stream=True to handle gzip content correctly if needed
        response = requests.get(url, headers=headers, timeout=30)

        print(f"2. Server responded with Status Code: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            
            # Check if valid playlist content exists
            if "#EXTM3U" in content:
                with open("iptv.m3u", "w", encoding="utf-8") as f:
                    f.write(content)
                print("✅ Success! Playlist saved to 'iptv.m3u'")
            else:
                print("⚠️ Server sent 200 OK, but content is not an M3U playlist.")
                print("First 200 chars of response:", content[:200])
                # We do NOT save the file if it's invalid, so git won't commit garbage.
        else:
            print(f"❌ Failed. Status Code: {response.status_code}")
            print("Response text:", response.text)
            
    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    fetch_playlist()
    
