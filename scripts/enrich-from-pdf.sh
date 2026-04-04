#!/usr/bin/env bash
# enrich-from-pdf.sh — PostToolUse hook for Write on raw/**/*.md
# Checks if a newly written raw/ file has an arxiv source URL,
# downloads the PDF, extracts text via pdftotext, appends to the .md,
# then deletes the PDF. Only runs for arxiv PDFs.
set -euo pipefail

# Read hook input from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only process raw/ markdown files
[[ "$FILE_PATH" == */raw/*.md ]] || exit 0

# Extract arxiv ID from frontmatter (use absolute paths to avoid rtk interception)
ARXIV_ID=$(/usr/bin/grep -m1 '^arxiv:' "$FILE_PATH" 2>/dev/null | /usr/bin/sed 's/arxiv: *"\{0,1\}\([^"]*\)"\{0,1\}/\1/' || true)
[[ -n "$ARXIV_ID" ]] || exit 0

# Check if file already has substantial content (>80 lines = probably already enriched)
LINE_COUNT=$(wc -l < "$FILE_PATH")
if [[ "$LINE_COUNT" -gt 80 ]]; then
  exit 0
fi

# Download PDF to temp
TMP_PDF=$(mktemp /tmp/arxiv-XXXXXX.pdf)
TMP_TXT=$(mktemp /tmp/arxiv-XXXXXX.txt)
trap 'rm -f "$TMP_PDF" "$TMP_TXT"' EXIT

if ! curl -sL -o "$TMP_PDF" "https://arxiv.org/pdf/${ARXIV_ID}" 2>/dev/null; then
  exit 0
fi

# Check it's actually a PDF (not an HTML error page)
if ! file "$TMP_PDF" | /usr/bin/grep -q PDF; then
  exit 0
fi

# Extract text
if ! pdftotext "$TMP_PDF" "$TMP_TXT" 2>/dev/null; then
  exit 0
fi

# Get page count
PAGES=$(pdfinfo "$TMP_PDF" 2>/dev/null | /usr/bin/grep -i pages | awk '{print $2}' || echo "?")

# Append extracted text to the .md file
{
  echo ""
  echo "---"
  echo ""
  echo "## Full Text (extracted from PDF, ${PAGES} pages)"
  echo ""
  cat "$TMP_TXT"
} >> "$FILE_PATH"

# Report via hook output
echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"PDF enrichment: downloaded arxiv/${ARXIV_ID} (${PAGES} pages), extracted and appended full text to ${FILE_PATH}.\"}}"
