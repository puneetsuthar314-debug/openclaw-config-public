---
name: content-fetcher
description: "Unified content fetcher for any URL. Extracts clean articles, downloads files (videos, images, PDFs), and fetches transcripts. Use when the user wants to download, extract, save, or get content from a URL. Triggers: download, extract, save, fetch, get content from URL, 抓取, 下载, 提取."
allowed-tools: [shell, file]
---

# Unified Content Fetcher

This skill provides a universal workflow to download, extract, or fetch any content from a given URL. It intelligently determines the content type and uses the best tool for the job.

## Primary Workflow

1.  **Analyze URL**: Determine the type of content at the URL (e.g., web page, video, direct file download, PDF).
2.  **Select Strategy**: Based on the content type, choose the appropriate extraction or download method.
3.  **Execute**: Run the chosen tool to fetch the content.
4.  **Process & Save**: Clean up the fetched content, save it to a standardized location, and report back to the user.

## Step 1: Analyze URL

Use `curl` to inspect the `Content-Type` header and follow redirects to understand the final URL's nature.

```bash
# Get headers to identify content type (e.g., application/pdf, image/jpeg, text/html)
curl -sIL "TARGET_URL" | grep -iE "^content-type:|^location:"
```

Based on the `Content-Type` and URL domain (e.g., `youtube.com`), proceed to the appropriate strategy.

## Step 2 & 3: Select Strategy and Execute

Choose one of the following strategies based on the analysis.

### Strategy 1: Article/Web Page Content Extraction

Use this for `text/html` content to get clean, readable text.

**Tool Priority: `trafilatura` > `reader` > `curl+python`**

```bash
# Recommended: Use trafilatura for robust extraction
URL="TARGET_URL"
# Get title for filename
TITLE=$(trafilatura --url "$URL" --json | python3 -c "import json, sys; print(json.load(sys.stdin).get('title', 'content'))")
FILENAME=$(echo "$TITLE" | tr -cs 'a-zA-Z0-9' '_' | cut -c 1-80).md

# Extract main content and save
trafilatura --url "$URL" --output-format txt --no-comments > "$FILENAME"

echo "✓ Content extracted to $FILENAME"
head -n 10 "$FILENAME"
```

*   **Dynamic/JS-heavy sites**: If `trafilatura` fails, consider using a browser-based tool if available.

### Strategy 2: Video/Audio Download & Transcription

Use for video platform URLs (YouTube, Bilibili, etc.). The primary tool is `yt-dlp`.

**A. Download Video/Audio:**

```bash
URL="TARGET_URL"

# List available formats first
yt-dlp --list-formats "$URL"

# Download best quality video + audio
yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -o "%(title)s.%(ext)s" "$URL"

# Download audio only as MP3
yt-dlp -x --audio-format mp3 -o "%(title)s.%(ext)s" "$URL"
```

**B. Download YouTube Transcript:**

```bash
URL="YOUTUBE_URL"

# 1. List available subtitles
yt-dlp --list-subs "$URL"

# 2. Try to get manual subtitles (best quality)
yt-dlp --write-sub --skip-download -o "transcript" "$URL"

# 3. If manual fails, get auto-generated subtitles
yt-dlp --write-auto-sub --skip-download -o "transcript" "$URL"

# 4. Convert VTT to clean TXT (IMPORTANT: removes timestamps and duplicates)
VTT_FILE=$(ls transcript.*.vtt | head -n 1)
TXT_FILE="$(basename "$VTT_FILE" .vtt).txt"
python3 -c "
import sys, re
seen = set()
with open('$VTT_FILE', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or '-->' in line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        clean = re.sub('<[^>]*>', '', line).strip()
        if clean and clean not in seen:
            print(clean)
            seen.add(clean)
" > "$TXT_FILE"

rm "$VTT_FILE"
echo "✓ Transcript saved to $TXT_FILE"
```

### Strategy 3: Direct File Download (PDF, ZIP, Images)

Use for URLs pointing directly to a file (`application/pdf`, `image/jpeg`, etc.).

**Tool Priority: `aria2c` (for speed) > `wget` / `curl`**

```bash
# Use aria2c for fast, multi-threaded downloads
aria2c -x 16 -s 16 -d . "TARGET_URL"

# Fallback with wget
wget -c "TARGET_URL"
```

### Strategy 4: Image Gallery Download

Use for image gallery sites like Imgur, Pixiv, etc. The primary tool is `gallery-dl`.

```bash
gallery-dl "GALLERY_URL"
```

## Step 4: Process & Save

-   **Filenames**: Create clean, descriptive filenames from the content's title. Remove special characters.
-   **Paths**: Save content to a structured directory, e.g., `~/content/{type}/{filename}` where `type` is `articles`, `videos`, `images`.
-   **Verification**: Check that the file was created and is not empty (`ls -lh` and `file`).
-   **Report**: Inform the user of the outcome, including the final file path and a preview if applicable.

## Required Tools & Installation

Before executing, verify the necessary tools are installed. If not, install them.

-   **`trafilatura`**: `pip3 install trafilatura`
-   **`yt-dlp`**: `pip3 install yt-dlp`
-   **`gallery-dl`**: `pip3 install gallery-dl`
-   **`aria2c`**: `sudo apt-get install -y aria2`
-   **`reader-cli`**: `npm install -g @mozilla/readability-cli`

Always check for a command's existence before using it (e.g., `command -v trafilatura`).
