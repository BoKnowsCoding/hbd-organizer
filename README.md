# hbd-runner
 
 Runs xtream1101/humblebundle-downloader, then copies the best quality
 comic files from the download folder to a target folder, and renames them.

Stored items and best quality paths are remembered in a file named 
.comic-picker.json, stored in the provided source directory.

After copying, the target folder can be reorganized at will by the user, 
the files will not be re-copied unless .comic-picker.json is deleted.

hbd-runner.sh will run humblebundle-downloader, then comic-picker.py to 
deploy the comics. I made this to add to my crontab to schedule a daily 
download and deploy my comics to my curated comics folder when I buy a new 
comic bundle.

Note: This should also find any comics in non-comic bundles, so long as 
they are available in the bundle as CBR or CBZ files. Items are identified 
as comic book files if one of the available formats is CBZ or CBR, but PDFs
are still checked for better quality.
