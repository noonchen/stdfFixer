#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# STDF Fixer
# Author: noonchen @ Github
# Email: chennoon233@gmail.com
# License: GPL-3.0

from xml.dom import minidom

class BinDefinitionParser:
    
    def __init__(self, BinDefinition):
        self.HBinDict = {}
        self.SBinDict = {}
        self.success = True
        
        try:
            doc = minidom.parse(BinDefinition)
            HBIN_node = doc.getElementsByTagName("HardwareBins")[0]
            SBIN_node = doc.getElementsByTagName("SoftwareBins")[0]
            hlist = HBIN_node.getElementsByTagName("Bin")
            slist = SBIN_node.getElementsByTagName("Bin")
            
            self.HBinDict = self.getHBinDict(hlist)
            self.SBinDict = self.getSBinDict(slist, self.HBinDict)
        except FileNotFoundError:
            self.success = False


    def getHBinDict(self, nodelist):
        HBinDict = {}
        
        for bin in nodelist:
            BIN_NUM = int(bin.getAttribute("number"))
            BIN_NAM = bin.getAttribute("name")
            BIN_PF = "P" if bin.getAttribute("type") == "Pass" else ("F" if bin.getAttribute("type") == "Fail" else " ")
            HBinDict[BIN_NUM] = {"BIN_NAM": BIN_NAM, "BIN_PF":BIN_PF}
        return HBinDict


    def getSBinDict(self, nodelist, HBinDict):
        SBinDict = {}
        
        for bin in nodelist:
            BIN_NUM = int(bin.getAttribute("number"))
            BIN_NAM = bin.getAttribute("name")
            BIN_PF = HBinDict.get(int(bin.getAttribute("hardwareBin")), {}).get("BIN_PF", " ")
            SBinDict[BIN_NUM] = {"BIN_NAM": BIN_NAM, "BIN_PF":BIN_PF}
        return SBinDict
