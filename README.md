# HBD Organizer

**Organize files output by humblebundle-downloader.**

This is a collection of scripts that takes the download folder of [xtream1101/humblebundle-downloader](https://github.com/xtream1101/humblebundle-downloader), and organizes them for deployment to media library folders. In cases like comic books where there are various versions of a single bundle item, the script attempts to find the best quality among them. At this time, the process is exclusively for copying files until this project has been thoroughly tested on my own library.

Stored items and best quality paths are remembered in a file named .comic-picker.json, stored in the provided source directory.
After the initial organization, the target folder can be reorganized at will by the user, the files will not be re-copied unless .comic-picker.json is deleted.

There are occasional inconsistencies with how Humble groups items and files in their bundles that may cause a few files to slip through the cracks, but I already address some of the edge cases.

## How to use

### Requirements
Requires xtream1101's humblebundle-downloader to be installed, which can be installed with pip.

```pip install humblebundle-downloader```

### Installation

The repository can be cloned and run from their for the newest features, but I recommend using the well-tested versions that will be published to the releases page.
To use hbd-runner, simply change the variables in the beginning of the hbd-runner.sh file to your own source/target directories, and add hbd-runner.sh to your /etc/crontab file. I recommend keeping the current version somewhere like /opt just to ensure it is not accidentally deleted/moved.

## Organizer Scripts

### hbd-runner.sh

A simple shell script to run humblebundle-downloader, then the various Python scripts for organization. This was created for scheduling downloads and organization in the crontab. Using this to run hbd ensures that downloads are completed before the organizer scripts are run.

### comic-picker.py
Copies the best quality comic files from the download folder to a target folder, and renames them.
This project started with this script in mind, to deploy the best quality comics from my hbd download folder to my curated comics folder when I buy a new comic bundle.
This should also find any comics in non-comic bundles, so long as they are available in the bundle as CBR or CBZ files. Items are identified as comic book files if one of the available formats is CBZ or CBR, but PDFs are still checked for better quality.

### book-copier.py
To me, the convenience of having all available file types outweighs the very small file size of regular e-books, so this script is configured to download all versions of an e-book in folders named by the item title (should be the book's title) to be easily imported into Calibre. I don't know of a way to automatically import these into Calibre, so the output folder will still need to be manually imported in Calibre, selecting to import directories and sub-directories and choosing to assume all e-book files in a single folder are the same book.
