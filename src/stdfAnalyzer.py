#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# STDF Fixer
# Author: noonchen @ Github
# Email: chennoon233@gmail.com
# License: GPL-3.0

from dataclasses import dataclass
from copy import deepcopy
from pystdf import V4
from stdfBinDefinitionParser import BinDefinitionParser

# dataclass for the possible missing records
@dataclass
class PRR_data:
    HEAD_NUM: int = None
    SITE_NUM: int = None
    PART_FLG: int = 0b00011100
    NUM_TEST: int = 0
    HARD_BIN: int = 65535
    SOFT_BIN: int = 65535
    X_COORD: int = -32768
    Y_COORD: int = -32768
    TEST_T: int = 0
    PART_ID: str = ""
    PART_TXT: str = ""
    PART_FIX: str = ""


@dataclass
class WRR_data:
    HEAD_NUM: int = None
    SITE_GRP: int = 255
    FINISH_T: int = 0
    PART_CNT: int = 0
    GOOD_CNT: int = 0
    ABRT_CNT: int = 4294967295
    FUNC_CNT: int = 4294967295
    RTST_CNT: int = 4294967295
    WAFER_ID: str = ""
    FRAME_ID: str = ""
    MASK_ID: str = ""
    USR_DESC: str = ""
    EXC_DESC: str = ""

@dataclass
class TSR_data:
    HEAD_NUM: int = None
    SITE_NUM: int = None
    TEST_NUM: int = None
    TEST_NAM: str = ""
    TEST_TYP: str = " "
    EXEC_CNT: int = 0
    FAIL_CNT: int = 0
    # ignored fields
    ALRM_CNT: int = 4294967295
    OPT_FLAG: int = 0xFF
    SEQ_NAME: str = ""
    TEST_LBL: str = ""
    TEST_TIM: float = 0
    TEST_MIN: float = 0
    TEST_MAX: float = 0
    TST_SUMS: float = 0
    TST_SQRS: float = 0


@dataclass
class BR_data:
    HEAD_NUM: int = None
    SITE_NUM: int = None
    BIN_NUM: int = None
    BIN_NAM: str = ""
    BIN_PF: str = " "
    BIN_CNT: int = 0


@dataclass
class PCR_data:
    HEAD_NUM: int = None
    SITE_NUM: int = None
    PART_CNT: int = 0
    GOOD_CNT: int = 0
    # ignored fields
    ABRT_CNT: int = 4294967295
    FUNC_CNT: int = 4294967295
    RTST_CNT: int = 4294967295
    
    
@dataclass
class MRR_data:
    FINISH_T: int = 0
    DISP_COD: str = " "
    USR_DESC: str = ""
    EXC_DESC: str = ""
    
    
def getBRdict(d, cls, dAvailable, HEAD_NUM=None, SITE_NUM=None):
    BinDict = {}
    if dAvailable:
        for BIN_NUM, vDict in d.items():
            BinDict[BIN_NUM] = cls(HEAD_NUM=HEAD_NUM, 
                                SITE_NUM=SITE_NUM, 
                                BIN_NUM=BIN_NUM, 
                                BIN_NAM=vDict["BIN_NAM"], 
                                BIN_PF=vDict["BIN_PF"])
    return deepcopy(BinDict)

class stdfAnalyzer:
    
    def __init__(self, BinDefinition, QSignal=None):
        self.PIRcnt = 0
        self.PRRcnt = 0
        self.WIRcnt = 0
        self.WRRcnt = 0
        self.startTime = 0  # unit in sec, UNIX time
        self.sumTestTime = 0    # unit in msec
        self.LastRecTyp = None
        self.LastRecData = {}
        self.offset = 0
        # Func
        self.onRec = dict((recType, lambda **kargs: None)
                 for recType in V4.records)
        self.onRec[V4.mir] = self.onMIR
        self.onRec[V4.wir] = self.onWIR
        self.onRec[V4.pir] = self.onPIR
        self.onRec[V4.ptr] = self.onTR
        self.onRec[V4.ftr] = self.onTR
        self.onRec[V4.mpr] = self.onTR
        self.onRec[V4.prr] = self.onPRR
        self.onRec[V4.wrr] = self.onWRR
        # bin info from xml
        self.BD = BinDefinitionParser(BinDefinition)
        self.BDAvailable = self.BD.success
        # pyqt signal
        self.QSignal = QSignal
        # PRR & WRR & MRR
        self.PRR = PRR_data()
        self.WRR = WRR_data()
        self.MRR = MRR_data()
        # site summary
        self.siteTSR = {}   # key: site_num, v = {test_num: TSR_data}
        self.siteHBR = {}   # key: site_num, v = {hbin_num: BR_data}
        self.siteSBR = {}   # key: site_num, v = {sbin_num: BR_data}
        self.sitePCR = {}   # key: site_num, v = PCR_data
        # summary
        self.sumTSR = {}    # {test_num: TSR_data}
        self.sumHBR = getBRdict(self.BD.HBinDict, 
                                BR_data, 
                                self.BDAvailable, 
                                HEAD_NUM=255, 
                                SITE_NUM=0)    # {hbin_num: BR_data}
        self.sumSBR = getBRdict(self.BD.SBinDict, 
                                BR_data, 
                                self.BDAvailable, 
                                HEAD_NUM=255, 
                                SITE_NUM=0)    # {sbin_num: BR_data}
        self.sumPCR = PCR_data(HEAD_NUM=255, SITE_NUM=0) # PCR_data
        
        
    def before_begin(self, DataSource):
        pass
        
        
    def before_send(self, DataSource, data_from_parser):
        # data_from_parser: (RecInstance, valueList)
        recType, valueList, offset = data_from_parser
        self.LastRecData = dict(zip(recType.fieldNames, valueList)) # key: Record Field Name, v = Field Data
        
        self.onRec[recType](recType=recType, valueDict=self.LastRecData)   # update summary
        self.LastRecTyp = recType   # save the latest record type
        self.offset = offset
        
        
    def getMissingRecList(self):
        # info = {"PRR":False, "WRR":False, "siteSUM":False, "overallSUM":False, "MRR":False}
        info = []
        
        if self.LastRecTyp == V4.mrr:
            # a complete std file
            if self.QSignal != None: self.QSignal.message_printer.emit('''<br><b><span style="color:green">{}</span></b><br>'''.format("The input STD file is intact, no fix needed"))

        else:
            if self.PIRcnt == 0:
                # No test data, won't fix
                if self.QSignal != None: self.QSignal.message_printer.emit('''<br><b><span style="color:green">{}</span></b><br>'''.format("No test data found, no fix needed"))
            
            elif self.PIRcnt > self.PRRcnt:
                # PRR is missing, add all summary
                info = ["PRR"]
                # manually call the function to summarize the generated PRR
                vlist = [self.PRR.__dict__[fn] for fn in V4.prr.fieldNames]
                self.before_send(None, (V4.prr, vlist, self.offset))
                
                if self.WIRcnt > self.WRRcnt:
                    # For wafer test, WRR is guranteed missing if PRR is absent
                    info.append("WRR")
                info.extend(["siteSUM", "overallSUM", "MRR"])
            
            elif self.PIRcnt == self.PRRcnt:
                # the most common case
                if self.WIRcnt > self.WRRcnt:
                    # WRR's missing means all summary is lost
                    info.extend(["WRR", "siteSUM", "overallSUM", "MRR"])
                
                elif self.LastRecTyp == V4.pcr:
                    # This cases rarely happens
                    if self.LastRecData["HEAD_NUM"] != 255:
                        # dup records may exist
                        info.extend(["siteSUM", "overallSUM"])
                    info.append("MRR")
                
                elif self.LastRecTyp == V4.tsr or self.LastRecTyp == V4.hbr or self.LastRecTyp == V4.sbr:
                    if self.LastRecData["HEAD_NUM"] != 255:
                        info.append("siteSUM")
                    info.extend(["overallSUM", "MRR"])  # dup records may exist

                else:
                    # add all summary
                    info.extend(["siteSUM", "overallSUM", "MRR"])

            else:
                # this case should never trigger
                pass
            
        return info
        
        
    def display(self):
        print('''
              PIRcnt: %d
              PRRcnt: %d
              startTime: %d
              sumTestTime:%d
              LastRecTyp: %s
              
              siteTSR: %s
              siteHBR: %s
              siteSBR: %s
              sitePCR: %s
              sumTSR: %s
              sumHBR: %s
              sumSBR: %s
              sumPCR: %s
              '''
              %(self.PIRcnt, self.PRRcnt, self.startTime, self.sumTestTime, self.LastRecTyp.name, 
                   self.siteTSR, self.siteHBR, self.siteSBR, self.sitePCR, 
                   self.sumTSR, self.sumHBR, self.sumSBR, self.sumPCR))
        
        
    def onMIR(self, **kargs):
        valueDict = kargs.get("valueDict", {})
        
        self.startTime = valueDict["START_T"]
        
    
    def onWIR(self, **kargs):
        valueDict = kargs.get("valueDict", {})
        
        self.WIRcnt += 1
        # Reinit WRR stats
        self.WRR.HEAD_NUM = valueDict["HEAD_NUM"]
        self.WRR.SITE_GRP = valueDict["SITE_GRP"]
        self.WRR.FINISH_T = valueDict["START_T"]    # delta = 0
        self.WRR.PART_CNT = 0
        self.WRR.GOOD_CNT = 0
        self.WRR.WAFER_ID = valueDict["WAFER_ID"]
    
    
    def onPIR(self, **kargs):
        valueDict = kargs.get("valueDict", {})
        
        self.PIRcnt += 1
        # Reinit PRR stats
        self.PRR.HEAD_NUM = valueDict["HEAD_NUM"]
        self.PRR.SITE_NUM = valueDict["SITE_NUM"]
        self.PRR.NUM_TEST = 0
        self.PRR.PART_ID = str(self.PIRcnt)
        # update WRR stats
        self.WRR.PART_CNT += 1
        
    
    
    def onTR(self, **kargs):
        # on Test Record: PTR, FTR, MPR
        recType = kargs.get("recType", None)
        valueDict = kargs.get("valueDict", {})
        
        HEAD_NUM = valueDict["HEAD_NUM"]
        SITE_NUM = valueDict["SITE_NUM"]
        TEST_NUM = valueDict["TEST_NUM"]
        TEST_FLG = valueDict["TEST_FLG"]
        TEST_TXT = valueDict["TEST_TXT"]
        
        if recType == V4.ptr:
            TEST_TYP = "P"
        elif recType == V4.ftr:
            TEST_TYP = "F"
        elif recType == V4.mpr:
            TEST_TYP = "M"
        else:
            TEST_TYP = " "
        
        tmpTSRofSite = self.siteTSR.setdefault(SITE_NUM, {})
        
        tmpTSR_data_site = tmpTSRofSite.setdefault(TEST_NUM, 
                                                   TSR_data(HEAD_NUM=HEAD_NUM, SITE_NUM=SITE_NUM, TEST_NUM=TEST_NUM, TEST_NAM=TEST_TXT, TEST_TYP=TEST_TYP))
        tmpTSR_data_sum = self.sumTSR.setdefault(TEST_NUM, 
                                                 TSR_data(HEAD_NUM=255, SITE_NUM=SITE_NUM, TEST_NUM=TEST_NUM, TEST_NAM=TEST_TXT, TEST_TYP=TEST_TYP))

        tmpTSR_data_site.EXEC_CNT += 1
        tmpTSR_data_site.FAIL_CNT += 0 if (TEST_FLG == 0) else 1

        tmpTSR_data_sum.EXEC_CNT += 1
        tmpTSR_data_sum.FAIL_CNT += 0 if (TEST_FLG == 0) else 1
        
        self.PRR.NUM_TEST += 1
    
    
    def onPRR(self, **kargs):
        valueDict = kargs.get("valueDict", {})
        
        HEAD_NUM = valueDict["HEAD_NUM"]
        SITE_NUM = valueDict["SITE_NUM"]
        PART_FLG = valueDict["PART_FLG"]
        HARD_BIN = valueDict["HARD_BIN"]
        SOFT_BIN = valueDict["SOFT_BIN"]
        # X_COORD = valueDict["X_COORD"]
        # Y_COORD = valueDict["Y_COORD"]
        TEST_T = valueDict["TEST_T"]
        # PART_ID = valueDict["PART_ID"]
        BIN_PF = "P" if PART_FLG == 0 else "F"
        
        tmpHBRofSite = self.siteHBR.setdefault(SITE_NUM, getBRdict(self.BD.HBinDict, 
                                                                   BR_data, 
                                                                   self.BDAvailable, 
                                                                   HEAD_NUM=HEAD_NUM, 
                                                                   SITE_NUM=SITE_NUM))
        
        tmpSBRofSite = self.siteSBR.setdefault(SITE_NUM, getBRdict(self.BD.SBinDict, 
                                                                   BR_data, 
                                                                   self.BDAvailable, 
                                                                   HEAD_NUM=HEAD_NUM, 
                                                                   SITE_NUM=SITE_NUM))
        
        tmpHBR_data_site = tmpHBRofSite.setdefault(HARD_BIN, 
                                                   BR_data(HEAD_NUM=HEAD_NUM, SITE_NUM=SITE_NUM, BIN_NUM=HARD_BIN))
        tmpSBR_data_site = tmpSBRofSite.setdefault(SOFT_BIN, 
                                                   BR_data(HEAD_NUM=HEAD_NUM, SITE_NUM=SITE_NUM, BIN_NUM=SOFT_BIN))
        tmpPCR_data_site = self.sitePCR.setdefault(SITE_NUM, 
                                                   PCR_data(HEAD_NUM=HEAD_NUM, SITE_NUM=SITE_NUM))
        
        tmpHBR_data_sum = self.sumHBR.setdefault(HARD_BIN, 
                                                 BR_data(HEAD_NUM=255, SITE_NUM=SITE_NUM, BIN_NUM=HARD_BIN))
        tmpSBR_data_sum = self.sumSBR.setdefault(SOFT_BIN, 
                                                 BR_data(HEAD_NUM=255, SITE_NUM=SITE_NUM, BIN_NUM=SOFT_BIN))

        self.PRRcnt += 1
        
        tmpHBR_data_site.HEAD_NUM = HEAD_NUM
        tmpHBR_data_sum.HEAD_NUM = 255
        tmpHBR_data_site.SITE_NUM = SITE_NUM
        tmpHBR_data_sum.SITE_NUM = SITE_NUM
        tmpHBR_data_site.BIN_CNT += 1
        tmpHBR_data_sum.BIN_CNT += 1

        tmpSBR_data_site.HEAD_NUM = HEAD_NUM
        tmpSBR_data_sum.HEAD_NUM = 255
        tmpSBR_data_site.SITE_NUM = SITE_NUM
        tmpSBR_data_sum.SITE_NUM = SITE_NUM
        tmpSBR_data_site.BIN_CNT += 1
        tmpSBR_data_sum.BIN_CNT += 1
        
        if not self.BDAvailable:
            tmpHBR_data_site.BIN_PF = BIN_PF
            tmpHBR_data_sum.BIN_PF = BIN_PF
            tmpSBR_data_site.BIN_PF = BIN_PF
            tmpSBR_data_sum.BIN_PF = BIN_PF

        tmpPCR_data_site.PART_CNT += 1
        tmpPCR_data_site.GOOD_CNT += 1 if PART_FLG == 0 else 0
        self.sumPCR.PART_CNT += 1
        self.sumPCR.GOOD_CNT += 1 if PART_FLG == 0 else 0
        
        self.WRR.GOOD_CNT += 1 if PART_FLG == 0 else 0
        self.sumTestTime += TEST_T
        self.MRR.FINISH_T = int(self.startTime + self.sumTestTime/1000)
        
        
    def onWRR(self, **kargs):
        self.WRRcnt += 1
