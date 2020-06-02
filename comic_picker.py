"""
 Designed to be used in conjunction with xtream1101/humblebundle-downloader.
 Takes the download directory of that script, then copies the best quality 
 comic book files to a chosen directory.

 Any bundles 

"""

import sys
import os
import shutil


def traverseSource(source,target):
    for bundleName in os.listdir(source):
        if os.path.isdir(source+"/"+bundleName):
            # in case a bundle has a comic available only in PDF, we'll know it's a comic, not a book.
            guaranteed = ("Comic" in bundleName) or ("Manga" in bundleName)

            #print(bundleName," ",guaranteed)
            bundleSource=source+"/"+bundleName
            bundleTarget=target+"/"+bundleName
            traverseBundle(bundleSource,bundleTarget,guaranteed)

def traverseBundle(source,target,guaranteed):
    for itemName in os.listdir(source):
        #print("--",itemName)
        itemPath = source+"/"+itemName
        qualityPicker(itemPath,target,itemName,guaranteed)

def qualityPicker(source,target,itemName,guaranteed):
    bestPath = ""
    bestSize = 0
    bestExtension = ""

    for fileName in os.listdir(source):
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

    if guaranteed:
        #os.makedirs(target, exist_ok=True)
        #shutil.copyfile(bestPath,target+"/"+itemName+bestExtension)
        print(target+"/"+itemName+bestExtension)
        

#def compareSize()


if __name__ == "__main__":

    """
    if len(sys.argv) != 3:
        print("\nMissing parameters.\nUsage: ", sys.argv[0], " <path to source> <path to target>\n")
        exit(1)
    else:
        sourcepath = sys.argv[1]
        targetpath = sys.argv[2]
    """

    # TODO:remove hardcoded paths
    sourcepath = "/mnt/storage/archive/humble"
    targetpath = "/mnt/storage/working/humblebundle-picker/target"

    traverseSource(sourcepath,targetpath)

