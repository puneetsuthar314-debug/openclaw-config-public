---
name: learn-and-ship
description: A unified workflow to extract content from any URL (YouTube, article, PDF) and transform it into an actionable implementation plan using the Ship-Learn-Next framework. Use when the user wants to learn from a resource and turn it into concrete steps, using phrases like "learn this [URL]", "make this actionable [URL]", or "create a plan from this video/article".
allowed-tools: Bash,Read,Write
---

# Learn & Ship: From Content to Action

This skill provides a complete workflow to extract knowledge from online content and immediately turn it into a concrete, actionable plan based on the **Ship-Learn-Next** framework. It combines content extraction with structured action planning.

## When to Use This Skill

Activate when the user provides a URL and wants to:
- "Learn" from it and "implement" the advice.
- Turn it into an "action plan" or make it "actionable."
- Create a project or a series of steps based on the content.
- Understand and then immediately apply knowledge.

**Keywords**: learn this, make actionable, create a plan from, implement, turn into steps, ship, learn, next.

## The Unified Workflow

1.  **Detect Content Type**: Automatically determine if the URL is a YouTube video, an article, or a PDF.
2.  **Extract Content**: Use the best tool to get a clean text version of the content.
3.  **Define a Quest**: Work with the user to set a clear 4-8 week goal based on the content.
4.  **Create a Rep Plan**: Design a series of 5 iterative "reps" (shippable actions), starting with one that can be completed this week.
5.  **Save & Present**: Save the extracted content and the action plan to files and present a summary to the user.

---

## Step 1: Detect & Extract Content

This step uses the URL provided by the user to get the raw material for the action plan.

### URL Detection & Extraction Logic

```bash
#!/bin/bash

# Usage: ./extract_content.sh <URL>

URL="$1"

if [ -z "$URL" ]; then
    echo "Usage: ./extract_content.sh <URL>"
    exit 1
fi

echo "🧵 Starting content extraction..."

# --- Detect content type ---
if [[ "$URL" =~ youtube\.com/watch || "$URL" =~ youtu\.be/ || "$URL" =~ youtube\.com/shorts ]]; then
    CONTENT_TYPE="youtube"
elif [[ "$URL" =~ \.pdf$ ]] || curl -sI "$URL" | grep -iq "Content-Type: application/pdf"; then
    CONTENT_TYPE="pdf"
else
    CONTENT_TYPE="article"
fi
echo "📍 Detected type: $CONTENT_TYPE"

# --- Extract content by type ---
case $CONTENT_TYPE in
    youtube)
        echo "📺 Extracting YouTube transcript..."
        if ! command -v yt-dlp &> /dev/null; then echo "Installing yt-dlp..."; sudo pip3 install yt-dlp; fi
        VIDEO_TITLE=$(yt-dlp --print "%(title)s" "$URL" | tr '/:?"' '----' | cut -c 1-100)
        yt-dlp --write-auto-sub --skip-download --sub-langs en --output "temp_transcript" "$URL"
        python3 -c "
import sys, re, os
vtt_file = 'temp_transcript.en.vtt'
if not os.path.exists(vtt_file): sys.exit(1)
seen = set()
with open(vtt_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line or '-->' in line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        clean = re.sub('<[^>]*>', '', line).replace('&amp;', '&').strip()
        if clean and clean not in seen:
            print(clean)
            seen.add(clean)
" > "${VIDEO_TITLE}.txt"
        rm -f temp_transcript.en.vtt
        CONTENT_FILE="${VIDEO_TITLE}.txt"
        ;;

    article)
        echo "📄 Extracting article..."
        if ! command -v trafilatura &> /dev/null; then echo "Installing trafilatura..."; sudo pip3 install trafilatura; fi
        METADATA=$(trafilatura --URL "$URL" --json)
        ARTICLE_TITLE=$(echo "$METADATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('title', 'Article'))" | tr '/:?"' '----' | cut -c 1-100)
        trafilatura --URL "$URL" --output-format txt --no-comments > "${ARTICLE_TITLE}.txt"
        CONTENT_FILE="${ARTICLE_TITLE}.txt"
        ;;

    pdf)
        echo "📑 Downloading and extracting PDF..."
        if ! command -v pdftotext &> /dev/null; then echo "Installing poppler..."; sudo apt-get update && sudo apt-get install -y poppler-utils; fi
        PDF_FILENAME=$(basename "$URL" | cut -c 1-100)
        curl -L -o "$PDF_FILENAME" "$URL"
        CONTENT_FILE="${PDF_FILENAME%.pdf}.txt"
        pdftotext "$PDF_FILENAME" "$CONTENT_FILE"
        echo "Original PDF downloaded as '$PDF_FILENAME'. You can remove it if not needed."
        ;;
esac

if [ -f "$CONTENT_FILE" ]; then
    echo "✓ Content extracted successfully!"
    echo "Saved to: $CONTENT_FILE"
    # Make the filename available to the next step
    echo "CONTENT_FILE=$CONTENT_FILE" > extraction_vars.sh
else
    echo "❌ Error: Content extraction failed."
    exit 1
fi
```

---

## Step 2: Create the Ship-Learn-Next Action Plan

After extracting the content, use the **Ship-Learn-Next** framework to build an action plan. This turns passive reading into active doing.

### Core Framework: Ship-Learn-Next

1.  **SHIP** - Create something real (code, content, a demonstration).
2.  **LEARN** - Reflect on what happened and what you learned.
3.  **NEXT** - Plan the next iteration based on those learnings.

**Principle**: Learning is measured by doing better, not knowing more.

### Planning Workflow

1.  **Read the Content**: Analyze the extracted text file.
2.  **Extract Core Lessons**: Identify the key actionable principles and skills taught.
3.  **Define the Quest**: Ask the user: *"Based on this, what do you want to achieve in the next 4-8 weeks? What would a concrete success look like?"*
4.  **Design Rep 1**: Ask the user: *"What's the smallest version of this you could ship THIS WEEK?"* Make it concrete, completable in 1-7 days, and produce a real artifact.
5.  **Map Future Reps (2-5)**: Outline a progression where each rep adds one new element or level of difficulty.
6.  **Save the Plan**: Write the complete plan to a Markdown file.

### Action Plan Template

Use this structure when writing the plan to a `.md` file. The filename should be `Ship-Learn-Next Plan - [Brief Quest Title].md`.

```markdown
# Your Ship-Learn-Next Quest: [Title]

## Quest Overview
**Goal**: [What they want to achieve in 4-8 weeks]
**Source**: [The content that inspired this]
**Core Lessons**: [3-5 key actionable takeaways from content]

---

## Rep 1: [Specific, Shippable Goal for This Week]

**Ship Goal**: [Concrete deliverable, e.g., "Publish one blog post using the framework"]
**Timeline**: By [Date]
**Success Criteria**:
- [ ] [Specific, verifiable outcome 1]
- [ ] [Specific, verifiable outcome 2]

**What You'll Practice** (from the source content):
- [Skill/concept 1 from source material]
- [Skill/concept 2 from source material]

**Action Steps**:
1. [First concrete step]
2. [Second concrete step]
3. Ship it (publish/deploy/share/demonstrate).

**After Shipping - Reflection**:
Answer these questions:
- What actually happened?
- What worked? What didn't?
- What surprised you?
- Rate this rep: _/10
- What's one thing to try differently next time?

---

## Rep 2-5: The Path Ahead

**Rep 2**: [Brief description of the next iteration, building on Rep 1]
**Rep 3**: [Brief description]
**Rep 4**: [Brief description]
**Rep 5**: [Brief description]

*(Details will evolve based on what you learn in earlier reps.)*

---

## Remember

- This is about DOING, not just studying.
- Aim for progress, not perfection.
- You learn by shipping, reflecting, and iterating.

**Ready to ship Rep 1?**
```

---

## Step 3: Final Output

After completing the extraction and planning, present the results clearly to the user.

```
✅ Learn & Ship Workflow Complete!

📥 **Content Extracted:**
   - Saved to: `[filename.txt]`

📋 **Action Plan Created:**
   - Quest: `[Quest title]`
   - Saved to: `Ship-Learn-Next Plan - [Title].md`

🎯 **Your Mission for This Week (Rep 1):**
   - [Goal of Rep 1]

When will you ship it?
```
