import json
import subprocess

INPUT = "output/book.md"
CONFIG_FILE = "output/config.json"

md_to_pdf_config = {
    "pdfOptions": {
        "format": "A4",
        "margin": {"top": "25mm", "left": "20mm", "right": "20mm", "bottom": "25mm"},
        "displayHeaderFooter": True,
        "headerTemplate": '<div style="font-family: Arial, sans-serif; font-size: 9px; width: 100%; padding: 0 20mm; color: #95a5a6; display: flex; justify-content: space-between;"><span>Learning Companion</span><span class="date"></span></div>',
        "footerTemplate": '<div style="font-family: Arial, sans-serif; font-size: 9px; width: 100%; padding: 0 20mm; color: #7f8c8d; text-align: right;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    },
    "mdOptions": {"linkify": True},
}

with open(CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(md_to_pdf_config, f, indent=4)

command = ["md-to-pdf.cmd", INPUT, "--config-file", CONFIG_FILE]

try:
    subprocess.run(command, check=True)
    print("PDF created successfully.")
except subprocess.CalledProcessError as e:
    print(f"Compilation engine failed: {e}")