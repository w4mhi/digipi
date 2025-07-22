#!/bin/bash

# backup.sh — Copies files listed in the source file to a destination, preserving paths.

show_help() {
    echo "Usage: $0 -d <destination> -f <file>"
    echo
    echo "Options:"
    echo "  -d <destination>   Required: Target directory where files will be copied."
    echo "  -f <file>          Required: Text file containing relative paths of files to back up."
    echo "  -h                 Show this help message."
    exit 1
}

# Initialize variables
DEST=""
SOURCE_FILE=""

# Parse parameters
while getopts "d:f:h" opt; do
    case "$opt" in
        d) DEST="$OPTARG" ;;
        f) SOURCE_FILE="$OPTARG" ;;
        h) show_help ;;
        *) show_help ;;
    esac
done

# Validate input
if [ -z "$DEST" ] || [ -z "$SOURCE_FILE" ]; then
    echo "Error: Destination and source file must both be specified."
    show_help
fi

# Check source file existence
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file '$SOURCE_FILE' not found."
    exit 1
fi

# Begin processing
while IFS= read -r REL_PATH || [ -n "$REL_PATH" ]; do
    [[ -z "$REL_PATH" || "$REL_PATH" =~ ^# ]] && continue

    SRC_FILE="/$REL_PATH"
    DEST_FILE="$DEST/$REL_PATH"
    DEST_DIR="$(dirname "$DEST_FILE")"

    mkdir -p "$DEST_DIR"

    if [ -f "$SRC_FILE" ]; then
        cp "$SRC_FILE" "$DEST_FILE"
        echo "Copied: $SRC_FILE → $DEST_FILE"
    else
        echo "Missing: $SRC_FILE (not copied)"
    fi
done < "$SOURCE_FILE"