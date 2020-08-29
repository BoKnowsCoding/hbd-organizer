#!/bin/bash

# Simply copies the scripts into a folder in /opt/
# I have a cron job set to run from there, and I only want to run stable versions.

INSTALL_DIR="/opt/hbd-organizer"

mkdir -p "$INSTALL_DIR"

cd "$(dirname $0)"

cp "./hbd-runner.sh" "$INSTALL_DIR/hbd-runner.sh"
chmod +x "$INSTALL_DIR/hbd-runner.sh"

cp "./audio-extractor.py" "$INSTALL_DIR/audio-extractor.py"
cp "./book-copier.py" "$INSTALL_DIR/book-copier.py"
cp "./comic-picker.py" "$INSTALL_DIR/comic-picker.py"
