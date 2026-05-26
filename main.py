import subprocess
import sys

steps = [
    "python -m scripts.fetch_playlist",
    "python -m scripts.extract_transcripts",
    "python -m scripts.generate_chapters",
    "python -m scripts.compile_book",
    "python -m scripts.export_pdf",
]

if __name__ == "__main__":

    for step in steps:

        print(f"\nRunning: {step}")

        result = subprocess.run(
            step,
            shell=True
        )

        if result.returncode != 0:

            print(f"\nStep failed: {step}")
            print("Stopping execution.")

            sys.exit(1)

    print("\nAll steps completed successfully.")