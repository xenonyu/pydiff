from os import path
import json_tools
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
    diff = json_tools.diff(left, right)
    jsonPaths = []
    for r in diff:
        if 'replace' in r: 
            jsonPath = parsePath(r['replace'])
            jsonPaths.append(jsonPath + "=" + r['value'])
        if 'remove' in r:
            jsonPath = parsePath(r['remove'])
            jsonPaths.append(jsonPath + "=")
    return jsonPaths


if __name__ == '__main__':

    with open("./tests/left.omap", 'r') as f:
        left = json.load(f)
        # print(left)
        f.close()
    with open("./tests/right.omap", 'r') as f:
        right = json.load(f)
        # print(right)
        f.close()
    print(getJsonPaths(left, right))