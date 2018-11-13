import re
import xml.etree.ElementTree as ET

### UTILS ###

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def readConfigFile(fName):
    worldConfig = {}
    
    xmlTree = ET.parse(fName)
    root = xmlTree.getroot()
    if root.tag != "AuthorsWorldConfig":
        print("Config file corrupted. Terminating...\n")

    for child in root:
        worldConfig[child.tag] = child.text

    return worldConfig 