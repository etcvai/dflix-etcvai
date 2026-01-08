import requests

url = "https://akashgo.noobmaster.xyz/?api=iptv_m3u"

headers = {
    "Host": "akashgo.noobmaster.xyz",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.12.0",
    "X-Requested-With": "com.blaze.sportzfy" 
}

def fetch_playlist():
    try:
        print("1. Sending request...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"2. Status Code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            # Check if it looks like a playlist (contains #EXTM3U)
            if "#EXTM3U" in content:
                with open("iptv.m3u", "w", encoding="utf-8") as f:
                    f.write(content)
                print("✅ Success! Playlist saved.")
            else:
                print("⚠️ Server replied 200 OK, but content is not M3U.")
                print("Server said:", content[:200]) # Print start of message to debug
        else:
            print(f"❌ Failed. Server sent: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_playlist()
            
