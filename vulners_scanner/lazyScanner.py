#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'videns'
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')
import json
import re
import subprocess

VULNERS_LINKS = {'pkgChecker':'https://vulners.com/api/v3/audit/audit/',
                 'bulletin':'https://vulners.com/api/v3/search/id/?id=%s'}


class LazyScanner():
    def __init__(self):
        pass

    def sshCommand(self,cmd):
        cmdResult = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=DEVNULL, shell=True).communicate()[0]
        if isinstance(cmdResult, bytes):
            cmdResult = cmdResult.decode('utf8')
        return cmdResult



    def getOSInfo(self):
        version = self.sshCommand("cat /etc/os-release")
        if version:
            reFamily = re.search("^ID=\"?(\w+)\"?",version,re.MULTILINE)
            if reFamily:
                osFamily = reFamily.group(1).lower()
            else:
                return

            reVersion = re.search("^VERSION_ID=\"?(\w+)\"?",version,re.MULTILINE)
            if reVersion:
                osVersion = reVersion.group(1).lower()
            else:
                return
            return (osFamily, osVersion)

    def getPackages(self, osName):
        if osName in ('debian','ubuntu', 'kali'):
            cmd = "dpkg-query -W -f='${Package} ${Version} ${Architecture}\n'"
        elif osName in ('rhel', 'centos', 'oraclelinux', 'suse', 'fedora'):
            cmd = "rpm -qa"
        else:
            cmd = None
        return self.sshCommand(cmd).splitlines() if cmd else None


    def auditSystem(self):
        osInfo = self.getOSInfo()
        if not osInfo:
            print("Can't detect OS, try linuxScanner.py instead")
            return
        print("OS Name - %s, OS Version - %s" % (osInfo[0], osInfo[1]))

        installedPackages = self.getPackages(osInfo[0])
        if not installedPackages:
            print("Couldn't find packages")
            return

        print("Total provided packages: %s" % len(installedPackages))
        # Get vulnerability information
        payload = {'os':osInfo[0],
                   'version':osInfo[1],
                   'package':installedPackages}
        req = urllib2.Request(VULNERS_LINKS.get('pkgChecker'))
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'vulners-lazy-scanner-v0.1')
        response = urllib2.urlopen(req, json.dumps(payload).encode('utf-8'))
        responseData = response.read()
        if isinstance(responseData, bytes):
            responseData = responseData.decode('utf8')
        responseData = json.loads(responseData)
        resultCode = responseData.get("result")
        if resultCode == "OK":
            print(json.dumps(responseData, indent=4))
            print("Vulnerabilities:\n%s" % "\n".join(responseData.get('data').get('vulnerabilities')))
        else:
            print("Error - %s" % responseData.get('data').get('error'))
        return

if __name__ == "__main__":
    scanner = LazyScanner()
    scanner.auditSystem()