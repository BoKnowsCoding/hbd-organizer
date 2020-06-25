"""
 Designed to be used in conjunction with xtream1101/humblebundle-downloader.
 Takes the download directory of that script, then copies all file types of 
 each non-comic book to a chosen directory.
 
 Each folder in the target directory will be one book, containing the 
 different file formats available for the book. They are not separated by 
 bundles, since this way you can import directories and subdirectories in 
 calibre, then choose to assume all e-book files in a directory are the same 
 book in different formats.

 Renaming files after they are copied will not result in files being copied
 again, as this script keeps a JSON in the given source directory recording 
 all files previously copied to a target folder.

"""

import sys
import os
import shutil
import json


def traverseBundles(source,target,hbdJSON,copiedJSON):
    for bundleName in os.listdir(source):
        bundleSource = source+"/"+bundleName
        bundleTarget = target
        
        # I don't think any comic bundles have regular books in them.
        if os.path.isdir(bundleSource) and "comic" not in bundleName.lower():
            traverseBundleItems(bundleSource,bundleTarget,hbdJSON,copiedJSON)

def traverseBundleItems(source,target,hbdJSON,copiedJSON):
    for itemName in os.listdir(source):
        if itemName not in copiedJSON:
            itemPath = source+"/"+itemName
            itemTarget = target+"/"+itemName
            traverseFiles(itemPath,itemTarget,hbdJSON,copiedJSON,itemName)

def traverseFiles(source,target,hbdJSON,copiedJSON,itemName):
    isComic = False
    isBook = False
    copyList = []

    if "comic" in itemName.lower():
        isComic = True


    for fileName in os.listdir(source):
        extension = os.path.splitext(fileName)[1]

        # if the item is available as a .cb* file, it's most likely a comic book
        # if there is no extension, it's probably a binary
        if extension is "":
            break
        elif ".cb" in extension:
            isComic = True
            break
        elif extension in ".pdf.epub.mobi":
            isBook = True
            copyList.append((source+"/"+fileName,target+"/"+fileName))
    
    if (isBook) and (not isComic) and (copyList):
        os.makedirs(target, exist_ok=True)
        copyFiles(itemName,copyList)
        copiedDict.update({itemName:"book"})


def copyFiles(itemName,copyList):
    if copyList:
        for copyJob in copyList:
            shutil.copyfile(copyJob[0],copyJob[1])
            print(copyJob[0]+"\n-->"+copyJob[1]+"\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nInvalid parameters.\nUsage: ", sys.argv[0], " <path to source> <path to target>\n")
        exit(1)
    else:
        source = sys.argv[1]
        target = sys.argv[2]
    
    with open(source+"/.cache.json") as hbdJsonFile:
        hbdDict = json.load(hbdJsonFile)
    
    if os.path.exists(source+"/.book-copier.json"):
        with open(source+"/.book-copier.json") as copiedJsonFile:
            copiedDict = json.load(copiedJsonFile)
    else:
        copiedDict = {}

    traverseBundles(source,target,hbdDict,copiedDict)

    with open(source+"/.book-copier.json","w") as copiedJsonFile:
        copiedJsonFile.write(json.dumps(copiedDict, sort_keys=True, indent=4))
