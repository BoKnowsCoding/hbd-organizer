"""
 Designed to be used in conjunction with xtream1101/humblebundle-downloader.
 Takes the download directory of that script, then copies the best quality 
 comic book files to a chosen directory.

 Renaming files after they are copied will not result in files being copied
 again, as this script keeps a JSON in the given source directory recording 
 all files previously copied to a target folder.

 If not all of the files in a bundle item are completed downloading, this may
 save another version of the item later if a better quality version is 
 downloaded. I recommend using the included hbd-runner.sh, which runs hbd 
 then the picker scripts.

"""

import sys
import os
import shutil
import json


def traverseBundles(source,comicsTarget,mangaTarget,hbdJSON,copiedJSON):
    for bundleName in os.listdir(source):
        bundleSource=source+"/"+bundleName
        if os.path.isdir(bundleSource):
            guaranteed = False
            targetName=bundleName
            
            # If bundle has a comic available only in PDF, we'll know it's a comic if
            # the bundle name contains "Comic" or "Manga".
            # Sometimes manga has "Comics" in the bundle name, so we check for manga first
            if "Manga" in bundleName:
                guaranteed = True
                bundleTarget = mangaTarget
            else:
                if "Comic" in bundleName:
                    guaranteed = True
                # Even if "Comic" isn't in the name, we still need to set a target directory,
                # so we will assume whatever we find in this bundle is a comic from this point.
                # The target folder will only be made if we find a verified comic file later.
                bundleTarget = comicsTarget
            
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
    
    if "comic" in itemName.lower() or ("graphic" in itemName.lower() and "novel" in itemName.lower()):
        guaranteed = True

    for fileName in os.listdir(source):
        extension = os.path.splitext(fileName)[1]
        filePath = source+"/"+fileName

        # if the item is available as a .cb* file, it's most likely a comic book
        if ".cb" in extension or "comic" in fileName.lower()  or ("graphic" in fileName.lower() and "novel" in fileName.lower()):
            guaranteed = True
        
        # I prefer cbz for compatibility, so those will be preferred when quality is equal
        if extension.lower() in ".cbz.cbr.pdf":
            fileSize = os.path.getsize(filePath)
            # If size is significantly greater, this is the new best file
            if (fileSize > (bestSize * 1.2)):
                bestPath = filePath
                bestSize = fileSize
                bestExtension = extension
            # If the size is comparable, then the preferred format is taken
            elif (fileSize > (bestSize * 0.9)) and (fileSize < (bestSize * 1.2)):
                if extension == ".cbz":
                    bestPath = filePath
                    bestSize = fileSize
                    bestExtension = extension
                elif (extension == ".cbr") and (bestExtension == ".pdf"):
                    bestPath = filePath
                    bestSize = fileSize
                    bestExtension = extension

    bestTarget = target+"/"+itemName+bestExtension
    if guaranteed:
        os.makedirs(target, exist_ok=True)
        shutil.copyfile(bestPath,bestTarget)
        copiedDict.update({itemName:bestPath})
        print(bestPath+"\n-->"+bestTarget+"\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\nInvalid parameters.\nUsage: ", sys.argv[0], " <path to source> <path to comics target> <path to manga target>\n")
        exit(1)
    else:
        source = sys.argv[1]
        targetComics = sys.argv[2]
        targetManga = sys.argv[3]
    
    with open(source+"/.cache.json") as hbdJsonFile:
        hbdDict = json.load(hbdJsonFile)
    
    if os.path.exists(source+"/.comic-picker.json"):
        with open(source+"/.comic-picker.json") as copiedJsonFile:
            copiedDict = json.load(copiedJsonFile)
    else:
        copiedDict = {}

    traverseBundles(source,targetComics,targetManga,hbdDict,copiedDict)

    with open(source+"/.comic-picker.json","w") as copiedJsonFile:
        copiedJsonFile.write(json.dumps(copiedDict, sort_keys=True, indent=4))
