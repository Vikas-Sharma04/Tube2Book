import glob
import json
import os
import re

OUTPUT_FILE = "output/book.md"

def to_title_case(text):
    """
    Converts text to standard book title case.
    Capitalizes major words, keeps specified minor words lowercase.
    """
    minor_words = {
        'a', 'an', 'the', 
        'and', 'but', 'or', 'for', 'nor', 'on', 'in', 
        'at', 'to', 'by', 'of', 'with', 'from', 'as',
        'is', 'are', 'am', 'was', 'were', 'be', 'been', 'being',
        'do', 'does', 'did', 'has', 'have', 'had', 'can', 'could',
        'will', 'would', 'shall', 'should', 'may', 'might', 'must',
        'about', 'through', 'over', 'into'
    }
    
    words = text.strip().split()
    if not words:
        return ""
    
    formatted_words = [words[0].capitalize()]
    
    for word in words[1:]:
        clean_word = re.sub(r'[^\w]', '', word.lower())
        
        if clean_word in minor_words:
            formatted_words.append(word.lower())
        else:
            formatted_words.append(word.capitalize())
            
    return " ".join(formatted_words)


# 1. Load data safely
with open("data/playlist_title.txt", "r", encoding="utf-8") as f:
    playlist_title = to_title_case(f.read().strip()) 

try:
    with open("data/videos.json", "r", encoding="utf-8") as f:
        videos = json.load(f)
except Exception:
    videos = []

# 2. Process and clean chapter titles defensively
chapter_titles = []
for video in videos:
    title = re.sub(
        r"^Lecture\s*\d+\s*:\s*",
        "",
        video["title"],
        flags=re.IGNORECASE,
    )
    chapter_titles.append(to_title_case(title))


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    
    # Gathers files that actually exist to prevent index out of bounds crashes
    chapter_files = sorted(glob.glob("data/chapters/*.md"))

    final_book = f"""<style>
/* --- Page Setup & Geometry --- */
@page {{
    size: A4;
    margin: 25mm 20mm 25mm 20mm;
    
    @bottom-right {{
        content: counter(page);
        font-family: "Helvetica Neue", Arial, sans-serif;
        font-size: 11px;
        color: #7f8c8d;
    }}
    @top-left {{
        content: "{playlist_title}";
        font-family: "Helvetica Neue", Arial, sans-serif;
        font-size: 11px;
        color: #95a5a6;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
}}

/* Cover Page Overrides (No Headers/Footers) */
@page :first {{
    margin: 0;
    @bottom-right {{ content: normal; }}
    @top-left {{ content: normal; }}
}}

/* --- Typography & Global Layout --- */
body {{
    font-family: "Georgia", "Times New Roman", serif;
    font-size: 15px;
    line-height: 1.7;
    color: #2c3e50;
    background-color: #ffffff;
    -webkit-font-smoothing: antialiased;
}}

h1, h2, h3, h4 {{
    font-family: "Helvetica Neue", "Arial", sans-serif;
    color: #1a252f;
    font-weight: 700;
    line-height: 1.3;
    page-break-after: avoid;
}}

h1 {{
    font-size: 30px;
    margin-top: 0;
    margin-bottom: 18px;
}}

h2 {{
    font-size: 22px;
    margin-top: 32px;
    margin-bottom: 14px;
    border-bottom: 1px solid #ecf0f1;
    padding-bottom: 6px;
}}

p {{
    margin-top: 0;
    margin-bottom: 18px;
    text-align: justify;
}}

/* --- Code Styling Fixes --- */
code {{
    font-family: "Courier New", Courier, monospace;
    background-color: #f8f9fa;
    padding: 3px 6px;
    border-radius: 4px;
    font-size: 85%;
    color: #c7254e;
}}

pre {{
    background-color: #f8f9fa;
    border: 1px solid #e1e8ed;
    border-radius: 6px;
    padding: 14px;
    margin-bottom: 18px;
    page-break-inside: avoid;
}}

pre code {{
    background-color: transparent;
    padding: 0;
    color: #333;
    font-size: 13px;
}}

/* --- Structural Components --- */
.title-page {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 0 12%;
    page-break-after: always;
    background: linear-gradient(135deg, #1a252f 0%, #2c3e50 100%);
}}

.title-page h1 {{
    font-size: 42px;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 16px;
    font-family: "Helvetica Neue", Arial, sans-serif;
}}

.title-page .subtitle {{
    font-size: 18px;
    color: #bdc3c7;
    font-weight: 300;
    letter-spacing: 1px;
}}

.toc {{
    padding-top: 20px;
    page-break-after: always;
}}

.toc h1 {{
    font-size: 26px;
    border-bottom: 2px solid #2c3e50;
    padding-bottom: 8px;
    margin-bottom: 28px;
}}

.toc-list {{
    list-style-type: none;
    padding-left: 0;
}}

.toc-list li {{
    margin-bottom: 16px;
    font-size: 16px;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dotted #dcdde1;
    padding-bottom: 4px;
}}

.toc-title {{
    background: #fff;
    padding-right: 5px;
}}

.toc-number {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-weight: bold;
    color: #7f8c8d;
    margin-right: 10px;
}}

.chapter-page {{
    page-break-before: always;
    padding-top: 10px;
}}

.chapter-header {{
    text-align: left;
    margin-bottom: 45px;
    border-bottom: 2px solid #2c3e50;
    padding-bottom: 20px;
}}

.chapter-number {{
    font-family: "Helvetica Neue", "Arial", sans-serif;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #7f8c8d;
    margin-bottom: 10px;
    font-weight: 600;
}}

.chapter-header h1 {{
    font-size: 34px;
    margin: 0;
    color: #2c3e50;
}}
</style>
"""

    final_book += f"""
<div class="title-page">
    <h1>{playlist_title}</h1>
</div>
"""

    # 🌟 FIXED TOC LOOKUP:
    # Ensure TOC generation matches the length of real files on disk
    final_book += """
<div class="toc">
    <h1>Table of Contents</h1>
    <ul class="toc-list">
"""
    for idx in range(len(chapter_files)):
        title = chapter_titles[idx] if idx < len(chapter_titles) else f"Chapter {idx + 1}"
        final_book += f'        <li><span class="toc-title"><span class="toc-number">{idx + 1:02d}</span> {title}</span></li>\n'

    final_book += """    </ul>
</div>
"""

    # 🌟 FIXED CONTENT COUPLING:
    # Safely iterates over files to make sure single-video layouts are built perfectly
    for idx, file in enumerate(chapter_files, start=1):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read().strip()

        chapter_title = (
            chapter_titles[idx - 1]
            if (idx - 1) < len(chapter_titles)
            else f"Chapter {idx}"
        )

        final_book += f"""
<div id="chapter-{idx}" class="chapter-page">
    <div class="chapter-header">
        <div class="chapter-number">Chapter {idx:02d}</div>
        <h1>{chapter_title}</h1>
    </div>
    
    {content}

</div>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_book)

    print("Compiled markdown successfully.")