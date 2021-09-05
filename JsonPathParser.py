from os import path
import jsontool
import json
from typing import *

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class JsonParser(object):
    def __init__(self):
        self.nameSet = {
            "Id",
            "Enabled",
            "Name",
            "AllowedIdentityType",
            "ResourceLoopbackProtocols",
            "HighPrivilegedAccessProtocols",
            "ClientAccessProtocols",
            "PftAccessProtocols",
            "CallbackAccessProtocols",
            "ServiceAccessProtocols",
            "AuthorizationRules",
            "CrossTenantAccess",
            "Comment",
            "MajorVersion",
            "MinorVersion",
            "PolicyVersion",
            "Owners",
            "ApiUrlSurfaces",
            "ApiPermissions",
            "ApiPermissionsV2",
            "BaselinePermissions",
            "SettingFilePath",
            "WebConfigPath",
            "OAuthProcessSettings"
            "ActorAppId",
            "Enabled",
            "CreatedTime",
            "LastModifiedTime",
            "AppScopes",
            "AccountTypes",
            "AcceptedLinkedUsers",
            "AcceptedUserPermissions",
            "ScopedAcceptedUserPermissions",
            "AcceptedAppPermissions",
            "ScopedAcceptedAppPermissions",
            "IsRBACRequired",
            "AllowGlobalActorToken",
            "PopRequired",
            "IssuerScopes",
            "AppId",
            "AuthorizedAppPermission",
            "ScopedAuthorizedAppPermissions",
        }
        self.nameDict = {}
        for name in self.nameSet:
            self.nameDict[name.lower()] = name

    def parsePath(self, originPath: str):
        jsonPath = ""
        pathSets = originPath.split("/")
        for ps in pathSets:
            if ps.isdigit():
                jsonPath+= "[" + ps + "]"
            elif ps:
                if ps.lower() in self.nameDict: ps = self.nameDict[ps.lower()]
                jsonPath+= "/"
                jsonPath+= ps
            
        return jsonPath

    def getJsonPaths(self, left: json, right: json):
        diff = jsontool.diff(left, right)
        jsonPaths = []
        for r in diff:
            if 'replace' in r: 
                if r['value'] and type(r['value']) == str:
                    r['value'] = "'" + r['value'] + "'"
                jsonPath = self.parsePath(r['replace'])
                jsonPaths.append(jsonPath + "=" + str(r['value']))
            if 'remove' in r:
                jsonPath = self.parsePath(r['remove'])
                jsonPaths.append(jsonPath + "=")
            if 'add' in r:
                if r['value'] and type(r['value']) == str:
                    r['value'] = "'" + r['value'] + "'"
                jsonPath = self.parsePath(r['add'])
                if jsonPath[-1] == ']' and jsonPath[-3] == '[': jsonPath = jsonPath[:-3]
                jsonPaths.append(jsonPath + "+=" + str(r['value']))
        for i in range(len(jsonPaths)):
            jsonPaths[i] = "\"" + jsonPaths[i][1:] + "\""
        return jsonPaths


if __name__ == '__main__':

    with open("./tests/left.json", 'r') as f:
        left = json.load(f)
        # print(left)
        f.close()
    with open("./tests/right.json", 'r') as f:
        right = json.load(f)
        # print(right)
        f.close()
    JsonParser()
    res = (JsonParser().getJsonPaths(left, right))
    for line in res:
        print(line)