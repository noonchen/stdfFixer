#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# STDF Fixer
# Author: noonchen @ Github
# Email: chennoon233@gmail.com
# License: GPL-3.0

import time
import struct
from threading import Thread
from pystdf.Types import packFormatMap
from pystdf import V4
from pystdf.IO import Parser
from stdfAnalyzer import stdfAnalyzer


class stdfFixer:
    def __init__(self, input_path, output_path, BinDefinition="", QSignal=None):
        self.packFieldType = {
            "C1": self.packStructType,
            "B1": self.packStructType,
            "U1": self.packStructType,
            "U2": self.packStructType,
            "U4": self.packStructType,
            "U8": self.packStructType,
            "I1": self.packStructType,
            "I2": self.packStructType,
            "I4": self.packStructType,
            "I8": self.packStructType,
            "R4": self.packStructType,
            "R8": self.packStructType,
            "Cn": lambda f_type, data: self.packCn(data),
            "Bn": lambda f_type, data: self.packBn(data),
            "Dn": lambda f_type, data: None,     # Dn/Vn not in use
            "Vn": lambda f_type, data: None
            }
        self.outpath = output_path
        self.QSignal = QSignal
        
        start = time.time()#
        try:
            self.stdin = open(input_path, "rb")
            self.a = stdfAnalyzer(BinDefinition=BinDefinition, QSignal=QSignal)
            self.p = Parser(inp=self.stdin, QSignal=QSignal)
            self.p.addSink(self.a)
            self.p.parse()
            time.sleep(0.51) # wait for the last message
            self.fix()
        except Exception as e:
            if self.QSignal != None: self.QSignal.message_printer.emit('''<span style="color:red"><b>Error occurs:<br>{0!r}</b></span>'''.format(e))
        finally:
            end = time.time()#
            if self.QSignal != None: self.QSignal.message_printer.emit("Elapsed time: %.2f sec\n"%(end - start))

        
    def fix(self):
        if self.QSignal != None: 
            self.QSignal.message_printer.emit('''<br><span style="color:#3498DB">**{}**</span><br>'''.format("Analysis completed, start fixing..."))
            self.QSignal.pgbar_setter.emit(0)
        
        MissingRecList = self.a.getMissingRecList()
        
        if not len(MissingRecList) == 0:
            byteStream = b''
            for i, recs in enumerate(MissingRecList):
                if self.QSignal != None:
                    self.QSignal.message_printer.emit('''<span style="color:#3498DB">**{}**</span><br>'''.format("Generating missing " + recs))
                    self.QSignal.pgbar_setter.emit(int(100 * (i+1)/len(MissingRecList)))
                byteStream += self.getBytes(recs)
                
            # write into new file
            std_out = open(self.outpath, "wb+")
            self.copy_original(std_out)
            if self.QSignal != None: self.QSignal.message_printer.emit('''<br><span style="color:#3498DB">**{}**</span><br>'''.format("Writing missing data"))
            std_out.write(byteStream)
            std_out.close()
            if self.QSignal != None: self.QSignal.message_printer.emit('''<span style="color:green">Fix successfully! The file is located in<br><b><span style="color:#F39C12">{}</span></b></span><br>'''.format(self.outpath))
        
        self.stdin.close()        
        
        
    def copy_original(self, fout):
        if self.QSignal != None: self.QSignal.pgbar_setter.emit(0) # Init progressBar value
        self.p.inp.seek(0)
        bytes_per_read = int(1e6)    # 1M
        FormatSize = lambda num: "%d Bytes"%num if num < 1e3 else ("%.2f KB"%(num/1e3) if num < 1e6 else ("%.2f MB"%(num/1e6) if num < 1e9 else "%.2f GB"%(num/1e9)))
        
        while self.p.inp.tell() < self.a.offset:
            bytes_should_read = bytes_per_read if (self.p.inp.tell() + bytes_per_read < self.a.offset) else self.a.offset - self.p.inp.tell()
            fout.write( self.p.inp.read(bytes_should_read) )
            
            if self.QSignal != None: 
                text = "Copied <b>%s</b>, total <b>%s</b>"%(FormatSize(fout.tell()), FormatSize(self.a.offset))
                self.QSignal.message_printer.emit(text)
                self.QSignal.pgbar_setter.emit( int(100 * fout.tell()/self.a.offset) )
    
    
    def getBytes(self, recs):
        
        if recs == "PRR":
            return self.packData(V4.prr, self.a.PRR)

        elif recs == "WRR":
            return self.packData(V4.wrr, self.a.WRR)

        elif recs == "siteSUM":
            tmpBytes = b''
            for site in sorted(self.a.siteTSR.keys()):
                tmpBytes += self.THSP_toBytes(self.a.siteTSR[site], self.a.siteHBR[site], self.a.siteSBR[site], self.a.sitePCR[site])
            return tmpBytes
        
        elif recs == "overallSUM":
            return self.THSP_toBytes(self.a.sumTSR, self.a.sumHBR, self.a.sumSBR, self.a.sumPCR)
        
        elif recs == "MRR":
            return self.packData(V4.mrr, self.a.MRR)
        
        else:
            pass
        

    def THSP_toBytes(self, TSR_dict, HBR_dict, SBR_dict, PCR):
        byteOut = b''
        for TEST_NUM in sorted(TSR_dict.keys()):
            byteOut += self.packData(V4.tsr, TSR_dict[TEST_NUM])
        for HBin in sorted(HBR_dict.keys()):
            byteOut += self.packData(V4.hbr, HBR_dict[HBin])
        for SBin in sorted(SBR_dict.keys()):
            byteOut += self.packData(V4.sbr, SBR_dict[SBin])
        byteOut += self.packData(V4.pcr, PCR)
        
        return byteOut

    def packData(self, recType, Rec_data):
        recDataDict = Rec_data.__dict__
        
        rec_byte_data = b''
        for field_name, field_type in recType.fieldMap:
            if recType == V4.hbr or recType == V4.sbr:
                if field_name.startswith("HBIN") or field_name.startswith("SBIN"):
                    field_name = field_name[1:]           
            rec_byte_data += self.packFieldType[field_type](field_type, recDataDict[field_name])
            
        rec_byte_len = self.packFieldType["U2"]("U2", len(rec_byte_data))
        rec_byte_typ = self.packFieldType["U1"]("U1", recType.typ)
        rec_byte_sub = self.packFieldType["U1"]("U1", recType.sub)
        
        return rec_byte_len + rec_byte_typ + rec_byte_sub + rec_byte_data
        
    def packStructType(self, f_type, data):
        data = data.encode("ascii") if isinstance(data, str) else data
        return struct.pack(self.p.endian + packFormatMap[f_type], data)
    
    def packCn(self, data):
        s = struct.pack( self.p.endian + str(len(data)) + "s", data.encode("ascii"))
        l = self.packStructType("U1", len(s))
        return l + s
    
    def packBn(self, data):
        # Bn is only used in PRR during the fix, 
        # return default value if PRR needs to be generated
        return b''