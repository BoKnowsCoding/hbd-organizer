#!/bin/bash

# Replace these values as needed.

HBD_DOWNLOAD_PATH="/mnt/storage/archive/purchases/humble"

# all formats of a book will be added to <BOOK_DEPLOYMENT_PATH>/<NAME OF BOOK>/<filename>, to be imported into calibre manually
BOOK_DEPLOYMENT_PATH="/mnt/storage/media/books/new"

# items will be organized by bundle within these dirctories, so you may want to deploy to separate "humble" folders
COMIC_DEPLOYMENT_PATH="/mnt/storage/media/comics/.humble/comics"
MANGA_DEPLOYMENT_PATH="/mnt/storage/media/comics/.humble/manga"

# songs and audiobook files will be organized in folders of their album name, like <MUSIC_DEPLOYMENT_PATH>/Bastion/01 The song.mp3
MUSIC_DEPLOYMENT_PATH="/mnt/storage/media/audio/music"
AUDIOBOOK_DEPLOYMENT_PATH="/mnt/storage/media/audio/audiobooks"

# all output of the python scripts is output to this log, and refreshed each time hbd-runner.sh runs
LOGFILE="/mnt/storage/.logs/hbd.log"
COOKIE_FILE="./hbd-cookies.txt"

# change to directory of this script
cd "$(dirname "$0")"
(
flock -n 456 || exit 1
    hbd download --cookie-file "$COOKIE_FILE" --library-path "$HBD_DOWNLOAD_PATH" &> "$LOGFILE"
    python3 ./book-copier.py "$HBD_DOWNLOAD_PATH" "$BOOK_DEPLOYMENT_PATH" &>> "$LOGFILE"
    python3 ./comic-picker.py -v "$HBD_DOWNLOAD_PATH" "$COMIC_DEPLOYMENT_PATH" "$MANGA_DEPLOYMENT_PATH" &>> "$LOGFILE"
    python3 ./audio-extractor.py "$HBD_DOWNLOAD_PATH" "$MUSIC_DEPLOYMENT_PATH" "$AUDIOBOOK_DEPLOYMENT_PATH" &>> "$LOGFILE"
) 456>/var/lock/hbd-runner-lock
