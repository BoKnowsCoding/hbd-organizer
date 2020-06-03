"""
 Designed to be used in conjunction with xtream1101/humblebundle-downloader.
 Takes the download directory of that script, then copies the best quality 
 comic book files to a chosen directory. This does not prevent lower quality
 

 Renaming files after they are copied will not result in files being copied
 again, as this script keeps a JSON in the given source directory recording 
 all files previously copied to a target folder.

 If not all of the files in a bundle item are completed downloading, this may
 save another version of the item later if a better quality version is 
 downloaded. I recommend using the included hbd-runner.sh, which runs hbd 
 then this script to sort the comics.

"""

import sys
import os
import shutil
import json


def traverseBundles(source,target,hbdJSON,copiedJSON):
    for bundleName in os.listdir(source):
        bundleSource=source+"/"+bundleName
        bundleTarget = target
        if os.path.isdir(bundleSource):
            guaranteed = False
            targetName=bundleName
            
            # in case a bundle has a comic available only in PDF, we'll know it's a comic, not a book.
            if ("Manga" in bundleName) or ("Comic" in bundleName):
                guaranteed = True
            
            # separate manga and comics
            # sometimes manga has "comics" in the bundle name, so we check for manga first
            if ("Manga" in bundleName):
                bundleTarget = bundleTarget + "/manga/Humble"
            else:
                # assume this is a comic
                # the target will only be made if it is a verified comic file
                bundleTarget = bundleTarget + "/comics/Humble"
            
            # trimming extraneous "Humble * Bundle - " at beginning of bundle name
            if "Bundle - " in bundleName:
                targetName = bundleName.split(" - ",1)[1]
            elif bundleName.startswith("Humble "):
                targetName = bundleName.split("Humble ",1)[1]
            
            bundleTarget = bundleTarget+"/"+targetName
            traverseBundleItems(bundleSource,bundleTarget,hbdJSON,copiedJSON,guaranteed)

def traverseBundleItems(source,target,hbdJSON,copiedJSON,guaranteed):
    for itemName in os.listdir(source):
        if itemName not in copiedJSON:
            itemPath = source+"/"+itemName
            filePicker(itemPath,target,hbdJSON,copiedJSON,itemName,guaranteed)

def filePicker(source,target,hbdJSON,copiedJSON,itemName,guaranteed):
    bestPath = ""
    bestSize = 0
    bestExtension = ""
    incompleteDownload = False

    for fileName in os.listdir(source):
        # check if any of the items in this 
        incompleteDownload = fileName in hbdJSON

        extension = os.path.splitext(fileName)[1]
        filePath = source+"/"+fileName
        # if the item is available as a .cb* file, it's most likely a comic book
        if ".cb" in extension:
            guaranteed = True
        
        # I prefer cbz for compatibility, so those will be preferred when quality is equal
        if extension in ".cbz.cbr.pdf":
            fileSize = os.path.getsize(filePath)
            # If size is significantly greater, this is the new best file
            if (fileSize > (bestSize * 1.2)):
                bestPath = filePath
                bestSize = fileSize
                bestExtension = extension
            # If the size is comparable, then the preferred format is taken
            elif (fileSize > (bestSize * 0.9)) and (fileSize < (bestSize * 1.2)):
                if extension is ".cbz":
                    bestPath = filePath
                    bestSize = fileSize
                    bestExtension = extension
                elif (extension is ".cbr") and (bestExtension is ".pdf"):
                    bestPath = filePath
                    bestSize = fileSize
                    bestExtension = extension

    bestTarget = target+"/"+itemName+bestExtension

    if guaranteed and not incompleteDownload:
        copiedDict.update({itemName:bestPath})
        os.makedirs(target, exist_ok=True)
        shutil.copyfile(bestPath,bestTarget)
        print(bestPath,"\n-->",bestTarget)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nInvalid parameters.\nUsage: ", sys.argv[0], " <path to source> <path to target>\n")
        exit(1)
    else:
        source = sys.argv[1]
        target = sys.argv[2]
    
    with open(source+"/.cache.json") as hbdJsonFile:
        hbdDict = json.load(hbdJsonFile)
    
    if os.path.exists(source+"/.comic-picker.json"):
        with open(source+"/.comic-picker.json") as copiedJsonFile:
            copiedDict = json.load(copiedJsonFile)
    else:
        copiedDict = {}

    traverseBundles(source,target,hbdDict,copiedDict)

    with open(source+"/.comic-picker.json","w") as copiedJsonFile:
        copiedJsonFile.write(json.dumps(copiedDict, sort_keys=True, indent=4))
