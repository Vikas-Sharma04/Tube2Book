import json
import os
import re

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

# =========================================================
# FOLDERS
# =========================================================

DATA_DIR = "data"

TRANSCRIPT_DIR = os.path.join(
    DATA_DIR,
    "transcripts"
)

os.makedirs(
    TRANSCRIPT_DIR,
    exist_ok=True
)

# =========================================================
# LOAD VIDEOS
# =========================================================

VIDEOS_FILE = os.path.join(
    DATA_DIR,
    "videos.json"
)

with open(
    VIDEOS_FILE,
    "r",
    encoding="utf-8"
) as f:

    videos = json.load(f)

print(f"Found {len(videos)} videos.\n")

# =========================================================
# YOUTUBE TRANSCRIPT API
# =========================================================

api = YouTubeTranscriptApi()

# =========================================================
# CLEAN VTT SUBTITLES
# =========================================================

def clean_vtt(vtt_path):

    with open(
        vtt_path,
        "r",
        encoding="utf-8"
    ) as f:

        lines = f.readlines()

    cleaned_lines = []

    for line in lines:

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip timestamps
        if "-->" in line:
            continue

        # Skip WEBVTT header
        if line.startswith("WEBVTT"):
            continue

        # Skip numeric lines
        if line.isdigit():
            continue

        # Remove HTML tags
        line = re.sub(r"<.*?>", "", line)

        cleaned_lines.append(line)

    # Remove repeated lines
    final_lines = []

    previous = ""

    for line in cleaned_lines:

        if line != previous:

            final_lines.append(line)

        previous = line

    return "\n".join(final_lines)

# =========================================================
# DOWNLOAD SUBTITLES USING YT-DLP
# =========================================================

def download_subtitles(video_id):

    youtube_url = (
        f"https://www.youtube.com/watch?v={video_id}"
    )

    output_template = os.path.join(
        TRANSCRIPT_DIR,
        f"{video_id}"
    )

    ydl_opts = {
        "skip_download": True,
        "writeautomaticsub": True,
        "writesubtitles": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": output_template,
        "quiet": True,
        "noplaylist": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        ydl.download([youtube_url])

    # Find subtitle file
    for file in os.listdir(TRANSCRIPT_DIR):

        if (
            file.startswith(video_id)
            and file.endswith(".vtt")
        ):

            return os.path.join(
                TRANSCRIPT_DIR,
                file
            )

    return None

# =========================================================
# FETCH TRANSCRIPT USING API
# =========================================================

def fetch_transcript_api(video_id):

    transcript = api.fetch(video_id)

    text = " ".join(
        [x.text for x in transcript]
    )

    return text

# =========================================================
# FETCH TRANSCRIPT USING YT-DLP FALLBACK
# =========================================================

def fetch_transcript_ytdlp(video_id):

    subtitle_path = download_subtitles(
        video_id
    )

    if subtitle_path is None:

        raise Exception(
            "No subtitles found using yt-dlp."
        )

    transcript_text = clean_vtt(
        subtitle_path
    )

    # Cleanup
    if os.path.exists(subtitle_path):

        os.remove(subtitle_path)

    return transcript_text

# =========================================================
# MAIN LOOP
# =========================================================

for index, video in enumerate(videos):

    video_id = video["id"]
    title = video["title"]

    transcript_path = os.path.join(
        TRANSCRIPT_DIR,
        f"{video_id}.txt"
    )

    print("\n" + "=" * 80)
    print(f"[{index + 1}/{len(videos)}]")
    print(f"Processing: {title}")
    print("=" * 80)

    # =====================================================
    # SKIP EXISTING TRANSCRIPT
    # =====================================================

    if os.path.exists(transcript_path):

        print(
            "Transcript already exists. Skipping."
        )

        continue

    transcript_text = None

    # =====================================================
    # TRY YOUTUBE TRANSCRIPT API FIRST
    # =====================================================

    try:

        print(
            "Trying YouTube Transcript API..."
        )

        transcript_text = fetch_transcript_api(
            video_id
        )

        print(
            "Transcript fetched using API."
        )

    except Exception as api_error:

        print(
            f"API failed: {api_error}"
        )

        # =================================================
        # FALLBACK TO YT-DLP
        # =================================================

        try:

            print(
                "Trying yt-dlp fallback..."
            )

            transcript_text = (
                fetch_transcript_ytdlp(
                    video_id
                )
            )

            print(
                "Transcript fetched using yt-dlp."
            )

        except Exception as ytdlp_error:

            print(
                "\nBoth methods failed:"
            )

            print(
                f"yt-dlp Error: {ytdlp_error}"
            )

            continue

    # =====================================================
    # SAVE TRANSCRIPT
    # =====================================================

    try:

        with open(
            transcript_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(transcript_text)

        print(
            "Transcript saved successfully."
        )

    except Exception as save_error:

        print(
            f"Failed to save transcript: {save_error}"
        )

print("\n" + "=" * 60)
print("ALL VIDEOS COMPLETED")
print("=" * 60)