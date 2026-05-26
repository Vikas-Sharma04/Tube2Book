import json
import os
import subprocess
import sys

def fetch_content(url):
    command = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-single-json",
        url,
    ]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error fetching resource. yt-dlp stderr: {result.stderr}")
        sys.exit(1)
        
    extracted_data = json.loads(result.stdout)
    videos = []
    
    # ── CASE 1: The URL is a Playlist ─────────────────────────────────────────
    if "entries" in extracted_data:
        title = extracted_data.get("title") or "Compiled Playlist"
        
        for entry in extracted_data["entries"]:
            if entry: 
                videos.append({
                    "id": entry["id"],
                    "title": entry["title"],
                })
                
    # ── CASE 2: The URL is an Individual Video ────────────────────────────────
    else:
        title = extracted_data.get("title") or "Single Video Extraction"
        videos.append({
            "id": extracted_data["id"],
            "title": title,
        })
        
    return title, videos

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    playlist_url = os.environ.get("PLAYLIST_URL")

    if not playlist_url:
        playlist_url = input("Enter YouTube playlist URL: ")

    if not playlist_url:
        print("Error: No target URL provided.")
        sys.exit(1)

    content_title, videos = fetch_content(playlist_url)

    with open("data/videos.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)

    with open("data/playlist_title.txt", "w", encoding="utf-8") as f:
        f.write(content_title)

    print(f"\nSource Title: {content_title}")
    print(f"Enqueued {len(videos)} video asset(s) for the pipeline\n")