#!/bin/bash

# Replace these values as needed.

HBD_DOWNLOAD_PATH="/mnt/storage/archive/humble"

# books will be directly in this "new" folder, to be imported into calibre manually
BOOK_DEPLOYMENT_PATH="/mnt/storage/media/books/new"

# the comics directory will be under this one, along with manga, e.g. /books/comics and /books/manga
COMIC_DEPLOYMENT_PATH="/mnt/storage/media/books"

# all output of the python scripts is output to this log, and refreshed each time hbd-runner.sh runs
LOG_PATH="/mnt/storage/.logs"
COOKIE_FILE="./hbd-cookies.txt"

# change to directory of this script
cd "$(dirname "$0")"
hbd download --cookie-file "$COOKIE_FILE" --library-path "$HBD_DOWNLOAD_PATH" --progress &> "$LOG_PATH/hbd.log"
python3 ./book-copier.py "$HBD_DOWNLOAD_PATH" "$BOOK_DEPLOYMENT_PATH" &>> "$LOG_PATH/hbd.log"
python3 ./comic-picker.py "$HBD_DOWNLOAD_PATH" "$COMIC_DEPLOYMENT_PATH" &>> "$LOG_PATH/hbd.log"
