#!/bin/bash

# Replace the download locations with your own.

HBD_DOWNLOAD_PATH="/mnt/storage/archive/humble"
COMIC_DEPLOYMENT_PATH="/mnt/storage/media/books"
LOG_PATH="/mnt/storage/.logs"
COOKIE_FILE="./hbd-cookies.txt"

# change to directory of this script
cd "$(dirname "$0")"
hbd download --cookie-file "$COOKIE_FILE" --library-path "$HBD_DOWNLOAD_PATH" --progress &> "$LOG_PATH/hbd.log"
python3 ./comic-picker.py "$HBD_DOWNLOAD_PATH" "$COMIC_DEPLOYMENT_PATH" &> "$LOG_PATH/comic-picker.log"
