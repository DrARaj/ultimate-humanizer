#!/usr/bin/env bash
set -e

TARGET_DIR="${HOME}/.claude/skills/ultimate-humanizer"

echo "Installing ultimate-humanizer into ${TARGET_DIR}..."
mkdir -p "${HOME}/.claude/skills"

if [ -d "${TARGET_DIR}/.git" ]; then
    echo "Updating existing installation..."
    git -C "${TARGET_DIR}" pull --quiet
else
    git clone --quiet https://github.com/DrARaj/ultimate-humanizer.git "${TARGET_DIR}"
fi

echo "Ultimate Humanizer successfully installed!"
echo "Restart Claude Code to use /ultimate-humanizer"
