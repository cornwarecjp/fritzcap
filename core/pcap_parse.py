#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
##################################################################################
# Simple FritzCap python port
# Simplifies generation and examination of traces taken from AVM FritzBox and/or SpeedPort
# Traces can be examined using WireShark
# (c) neil.young 2010 (spongebob.squarepants in http://www.ip-phone-forum.de/)
# based on the Windows GUI exe with same name
##################################################################################

import struct, array

# http://wiki.wireshark.org/Development/LibpcapFileFormat
# but it doesn't say something about the "modified" format as provided by FritzBox and SpeedPort....


''' Parses PCAP files '''
class PcapParser:
    def __init__(self, filename, cb):
        self.f = open(filename, 'rb')       
        self.cb = cb
        
    def parse(self):
        # Read and check magic number
        # Details s.a.
        modified = 0
        try:
            mn, = struct.unpack('<L', self.f.read(4))
        except:
            print 'Seems, there is no valid PCAP file'
            return -1
        if mn == 0xa1b2c3d4 or mn == 0xa1b2cd34:        # Default or modified libpcap 
            # Little endian
            endian = '<'
            if mn == 0xa1b2cd34:
                modified = 1
        elif mn == 0xd4c3b2a1 or mn == 0x34cdb2a1:      # Default or modified libpcap 
            # Big endian
            endian = '>'
            if mn == 0x34cdb2a1:
                modified = 1
        else:
            print 'Invalid PCAP dump header. Probably not a valid capture file'
            return -1
        
        # Read the rest of the dumpheader   
        (vmj, vmi, z, sf, sl, nw) = struct.unpack(endian + 'HHlLLL', self.f.read(20))

        # Loop
        while True:
            # Read packet header
            ph = self.f.read(16)
            if not ph:
                break   # end of file
               
            # Get some values                
            (ts_sec, ts_usec, incl_len, orig_len) = struct.unpack(endian + 'LLLL', ph)

            if modified: 
                self.f.read(8)      # The way it is, don't know, why they had to change this plain old format
            
            self.cb(ts_sec, ts_usec, self.f.read(incl_len), incl_len)

