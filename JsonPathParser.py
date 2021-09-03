from os import path
import jsontool
import json
from typing import *

def parsePath(originPath: str):
    jsonPath = ""
    pathSets = originPath.split("/")
    for ps in pathSets:
        if ps.isdigit():
            jsonPath+= "[" + ps + "]"
        elif ps:
            jsonPath+= "/"
            jsonPath+= ps
        
    return jsonPath

def getJsonPaths(left: dict, right: dict):
    diff = jsontool.diff(left, right)
    jsonPaths = []
    for r in diff:
        if 'replace' in r: 
            jsonPath = parsePath(r['replace'])
            jsonPaths.append(jsonPath + "=" + str(r['value']))
        if 'remove' in r:
            jsonPath = parsePath(r['remove'])
            jsonPaths.append(jsonPath + "=")
        if 'add' in r:
            jsonPath = parsePath(r['add'])
            jsonPaths.append(jsonPath + "+=" + str(r['value']))
    jsonString = ""
    if jsonPaths:
        jsonString += "\"" + jsonPaths[0][1:] + "\""
    for jp in jsonPaths[1:]:
        jsonString += "," + "\n" + "\"" + jp[1:] + "\""
    return jsonString


if __name__ == '__main__':

    with open("./tests/left.json", 'r') as f:
        left = json.load(f)
        # print(left)
        f.close()
    with open("./tests/right.json", 'r') as f:
        right = json.load(f)
        # print(right)
        f.close()
    print(getJsonPaths(left, right))