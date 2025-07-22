#!/bin/bash

# restore.sh — Restores files from a backup directory to their original locations.

show_help() {
    echo "Usage: $0 -s <source> [-i]"
    echo
    echo "Options:"
    echo "  -s <source>    Required: Path to backup directory to restore from."
    echo "  -i             Optional: Interactive mode. Prompts before overwriting files."
    echo "  -h             Show help."
    exit 1
}

SOURCE=""
INTERACTIVE=false

while getopts "s:ih" opt; do
    case "$opt" in
        s) SOURCE="$OPTARG" ;;
        i) INTERACTIVE=true ;;
        h) show_help ;;
        *) show_help ;;
    esac
done

if [ -z "$SOURCE" ]; then
    echo "Error: You must specify a source path."
    show_help
fi

if [ ! -d "$SOURCE" ]; then
    echo "Error: '$SOURCE' is not a valid directory."
    exit 1
fi

echo "🔄 Restoring files from: $SOURCE"
echo

# Save list of files in an array to avoid piping issues with `read -p`
mapfile -t FILES < <(find "$SOURCE" -type f)

for SRC_FILE in "${FILES[@]}"; do
    REL_PATH="${SRC_FILE#$SOURCE/}"
    DEST_FILE="/$REL_PATH"
    DEST_DIR="$(dirname "$DEST_FILE")"

    mkdir -p "$DEST_DIR"

    if $INTERACTIVE && [ -f "$DEST_FILE" ]; then
        echo "File exists: $DEST_FILE"
        echo "Source → Destination:"
        echo "$SRC_FILE -> $DEST_FILE"
        read -r -p "Overwrite? [y/N]: " CONFIRM
        [[ "$CONFIRM" =~ ^[Yy]$ ]] || { echo "⏭️ Skipped: $DEST_FILE"; continue; }
    fi

    cp -f "$SRC_FILE" "$DEST_FILE"
    echo "$SRC_FILE → $DEST_FILE"
done

echo
echo "Restore complete."