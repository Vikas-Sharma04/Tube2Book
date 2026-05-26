import glob
import os
import time

from scripts.chunk_transcripts import (
    split_text_into_chunks,
)

from utils.helpers import save_text
from utils.mistral_client import generate_text


INPUT_DIR = "data/transcripts"
OUTPUT_DIR = "data/chapters"

PROMPT_FILE = "prompts/chapter_prompt.txt"

# =====================================================
# LOAD PROMPT
# =====================================================

with open(
    PROMPT_FILE,
    "r",
    encoding="utf-8"
) as f:

    CHAPTER_PROMPT = f.read()


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    files = glob.glob(
        f"{INPUT_DIR}/*.txt"
    )

    for file in files:

        filename = os.path.basename(file)

        filename = filename.replace(
            ".txt",
            ""
        )

        output_file = (
            f"{OUTPUT_DIR}/{filename}.md"
        )

        if os.path.exists(output_file):

            print(
                f"Skipping: {filename}"
            )

            continue

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            transcript = f.read()

        # =================================================
        # SPLIT INTO CHUNKS
        # =================================================

        chunks = split_text_into_chunks(
            transcript
        )

        chunk_sections = []

        print(
            f"\nGenerating sections "
            f"for {len(chunks)} chunks..."
        )

        # =================================================
        # GENERATE DETAILED SECTION FOR EACH CHUNK
        # =================================================

        for index, chunk in enumerate(chunks):

            print(
                f"Processing chunk "
                f"{index + 1}/{len(chunks)}"
            )

            prompt = f"""
{CHAPTER_PROMPT}

Transcript Chunk:

{chunk}
"""

            section = generate_text(prompt)

            chunk_sections.append(section)

            # Prevent rate limits
            time.sleep(5)

        # =================================================
        # MERGE GENERATED SECTIONS
        # =================================================

        final_chapter = "\n\n".join(
            chunk_sections
        )

        # =================================================
        # SAVE FINAL CHAPTER
        # =================================================

        save_text(
            output_file,
            final_chapter,
        )

        print(
            f"Saved chapter: "
            f"{filename}.md"
        )

        # Extra delay
        time.sleep(10)