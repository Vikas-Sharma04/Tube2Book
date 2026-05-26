# 📘 YouTube Video/Playlist → Ebook Generator

Turn long-form YouTube videos or playlists into structured, readable ebooks using AI models.

This project automatically extracts transcript content, processes large transcripts intelligently, generates AI-written chapters, and compiles everything into a clean Markdown/PDF ebook.

---

# ⚙️ Workflow

```text
YouTube Video / Playlist
            ↓
Metadata Extraction
            ↓
Subtitle / Transcript Extraction
            ↓
Transcript Cleaning
            ↓
Transcript Chunking
            ↓
Chunk Summarization
            ↓
Merged Context Generation
            ↓
Final Chapter Generation
            ↓
Markdown Ebook
            ↓
PDF Export
```

---

# ✨ Features

- Convert both single YouTube videos and playlists into ebooks  
- Automatic metadata extraction  
- Subtitle extraction using yt-dlp  
- Smart transcript chunking with overlap support  
- AI-powered chunk summarization pipeline  
- Generates textbook-style structured chapters  
- Handles extremely long transcripts efficiently  
- Markdown + PDF export  
- Modular and scalable architecture  
- Streamlit web interface included  
- CLI automation support  

---

# 🎯 Supported Input Types

| Type | Example |
|------|--------|
| Single Video | `https://www.youtube.com/watch?v=VIDEO_ID` |
| Playlist | `https://www.youtube.com/playlist?list=PLAYLIST_ID` |

---

# 🎧 Transcript Extraction

## Current Method
- yt-dlp subtitle extraction  

## Optional Alternatives & Future Integrations (User Configurable)

These are not used in the current pipeline but can be integrated:

- youtube-transcript-api  
- Whisper AI  
- OpenAI Whisper API  

---

# 🧠 AI Processing Pipeline

```text
Transcript
    ↓
Cleaning
    ↓
Chunking
    ↓
Chunk Summaries
    ↓
Merged Summaries
    ↓
Final Chapter Generation
    ↓
Book Compilation
```

---

# 📂 Project Structure

```
Tube2Book/
│
├── data/
│   ├── transcripts/
│   ├── chapters/
│   ├── videos.json
│   └── playlist_title.txt
│
├── output/
│   ├── book.md
│   └── book.pdf
│
├── prompts/
│   └── chapter_prompt.txt
│
├── scripts/
│   ├── fetch_content.py
│   ├── extract_transcripts.py
│   ├── chunk_transcripts.py
│   ├── generate_chapters.py
│   ├── compile_book.py
│   └── export_pdf.py
│
├── utils/
│   ├── helpers.py
│   └── mistral_client.py
│
├── main.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# 🚀 Installation

## 📥 Clone Repository

```bash
git clone <repo-url>
cd Tube2Book
```

---

## 🧪 Create Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS
```bash
python -m venv venv
source venv/bin/activate
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_api_key_here
```

---

# 🛠️ Usage

## 1️⃣ Fetch Video or Playlist Metadata

```bash
python -m scripts.fetch_content
```

---

## 2️⃣ Extract Transcripts

```bash
python -m scripts.extract_transcripts
```

---

## 3️⃣ Generate AI Chapters

```bash
python -m scripts.generate_chapters
```

---

## 4️⃣ Compile Book

```bash
python -m scripts.compile_book
```

---

## 5️⃣ Export PDF

```bash
python -m scripts.export_pdf
```

---

# ⚡ Run Full Pipeline

## 🖥️ Terminal Automation

```bash
python main.py
```

Runs the entire pipeline automatically.

---

## 🌐 Streamlit Web Application

```bash
streamlit run app.py
```

Launches the interactive browser-based UI.

---

# 📤 Output Files

| File | Description |
|------|------------|
| `output/book.md` | Generated ebook (Markdown) |
| `output/book.pdf` | Final PDF version |

---

# 💡 Example Use Cases

- Convert AI course playlists into study books  
- Generate notes from educational videos  
- Create technical documentation from tutorials  
- Turn long lectures into readable ebooks  
- Build personal knowledge archives  

---

# 🤖 Current AI Model

- Mistral AI models  

---

# 🔌 Optional Model Support

The architecture is fully modular, enabling easy integration of alternative AI models by modifying the model client file located in the `utils/` folder.

## ☁️ Cloud Models
- OpenAI GPT models  
- Google Gemini models  

## 🏠 Local/Open-Source Models
- Llama  
- Mistral Instruct  
- DeepSeek  
- Gemma  

---

# 🧰 Tech Stack

- Python  
- yt-dlp  
- Mistral AI  
- Streamlit  
- Markdown  
- PDF generation tools  

---

# ⚠️ Disclaimer

Generated ebooks depend on subtitle/transcript quality and AI model performance.  
Always review generated content before publishing or distribution.