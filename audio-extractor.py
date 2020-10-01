"""
 Extracts Audiobooks and Music from the download folder of humblebundle-downloader
 As far as I know, all audio files downloaded by hbd are in zip folders, so we'll look 
 for zip folders with either mp3 or flac in the filename.


"""


import sys
import os
import shutil
import json
import zipfile


def traverseBundles(source,music,audiobooks,hbdJSON,copiedJSON):
    for bundleName in os.listdir(source):
        bundleSource = source+"/"+bundleName
        if os.path.isdir(bundleSource):
            traverseBundleItems(bundleSource,music,audiobooks,hbdJSON,copiedJSON,bundleName)

def traverseBundleItems(source,music,audiobooks,hbdJSON,copiedJSON,bundleName):
    for itemName in os.listdir(source):
        if itemName not in copiedJSON:
            itemPath = source+"/"+itemName
            filePicker(itemPath,music,audiobooks,hbdJSON,copiedJSON,itemName,bundleName)

# picks the preferred file type, which should be part of the zip filename
def filePicker(source,music,audiobooks,hbdJSON,copiedJSON,itemName,bundleName):
    bestFile = ""
    bestType = ""
    for fileName in os.listdir(source):
        extension = os.path.splitext(fileName)[1]
        
        # look for zips and stop looking if we find flac
        if ".zip" in extension.lower():
            if "flac" in fileName.lower():
                bestFile = fileName
                bestType = "flac"
            elif "wav" in fileName.lower() and "flac" not in bestType:
                bestFile = fileName
                bestType = "wav"
            elif "mp3" in fileName.lower() and "flac" not in bestType and "wav" not in bestType:
                bestFile = fileName
                bestType = "mp3"
    if bestFile != "":
        if extractZip(source,music,audiobooks,itemName,bundleName,source+"/"+bestFile):
            copiedJSON.update({itemName:bestFile})

def extractZip(source,music,audiobooks,itemName,bundleName,filePath):
    with zipfile.ZipFile(filePath,"r") as myZip:
        if "audiobook" in bundleName.lower() or "audiobook" in itemName.lower():
            targetDir = audiobooks
        else:
            targetDir = music
        itemPath = targetDir+"/"+itemName
        myZip.extractall(itemPath)

    #clean up folder
    if len(os.listdir(itemPath)) == 1:
        subDirPath = itemPath+"/"+os.listdir(itemPath)[0]
        if os.path.isdir(subDirPath):
            for fileName in os.listdir(subDirPath):
                shutil.move(subDirPath+"/"+fileName, itemPath+"/"+fileName)
            os.rmdir(subDirPath)

    print(itemName)
    return True


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("\nInvalid parameters.\nUsage: ", sys.argv[0], " <path to source> <path to music target> <path to audiobook target>\n")
        exit(1)
    else:
        source = sys.argv[1]
        musicTarget = sys.argv[2]
        audiobookTarget = sys.argv[3]
    
    with open(source+"/.cache.json") as hbdJsonFile:
        hbdDict = json.load(hbdJsonFile)
    
    if os.path.exists(source+"/.audio-extractor.json"):
        with open(source+"/.audio-extractor.json") as copiedJsonFile:
            copiedDict = json.load(copiedJsonFile)
    else:
        copiedDict = {}

    traverseBundles(source,musicTarget,audiobookTarget,hbdDict,copiedDict)

    with open(source+"/.audio-extractor.json","w") as copiedJsonFile:
        copiedJsonFile.write(json.dumps(copiedDict, sort_keys=True, indent=4))