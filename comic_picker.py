# Designed to be used in conjunction with xtream1101/humblebundle-downloader.
# Takes the download directory of that script, then copies the best quality 
# comic book files to a chosen directory.

import sys
import os


if len(sys.argv) != 3:
    print("\nMissing parameters.\nUsage: ", sys.argv[0], " <path to source> <path to target>\n")
    exit(1)
else:
    sourcepath = sys.argv[1]
    targetpath = sys.argv[2]

for root, dirs,files in os.walk(sourcepath):  
    for fname in files:
        fpath = os.path.join(root,fname)
        
