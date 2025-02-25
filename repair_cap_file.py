#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#################################################################################
# This program repair the cap file if the captured data contains errors.
#
# usage:
#    repair_cap_file
#
# please edit this file to set the file_to_open and file to save
#
# (c) tom2bor 2011 (tom2bor in http://www.ip-phone-forum.de/)
##################################################################################
# Copyright (c) 2011, tom2bor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##################################################################################


import urllib.request, urllib.parse, urllib.error, re, timeit, hashlib, sys, datetime, os, struct, array

#typedef struct pcap_hdr_s {
#        guint32 magic_number;   /* magic number */
#        guint16 version_major;  /* major version number */
#        guint16 version_minor;  /* minor version number */
#        gint32  thiszone;       /* GMT to local correction */
#        guint32 sigfigs;        /* accuracy of timestamps */
#        guint32 snaplen;        /* max length of captured packets, in octets */
#        guint32 network;        /* data link type */
#} pcap_hdr_t;

#typedef struct pcaprec_hdr_s {
#        guint32 ts_sec;         /* timestamp seconds */
#        guint32 ts_usec;        /* timestamp microseconds */
#        guint32 incl_len;       /* number of octets of packet saved in file */
#        guint32 orig_len;       /* actual length of packet */
#} pcaprec_hdr_t;



def check_packet_header_buff(ph, last_time_sec, snaplen):
    (ts_sec, ts_usec, incl_len, orig_len) = struct.unpack(endian + 'LLLL', ph)
    cap_time = datetime.datetime.fromtimestamp(ts_sec)

    if (last_time_sec <= 0):
        delta_time = 0
    else:
        delta_time = last_time_sec - ts_sec
        if (delta_time < 0):
            delta_time = -delta_time

    if (incl_len == orig_len and incl_len <= snaplen and incl_len > 0 and delta_time < 1000):
        return (ts_sec, ts_usec, incl_len, orig_len, True)
    return (ts_sec, ts_usec, incl_len, orig_len, False)

def check_packet_header(f, counter, snaplen, filepos):
    save_current_file_pos = f.tell()
    f.seek(filepos)
    ph = f.read(16)
    f.seek(save_current_file_pos)

    (ts_sec, ts_usec, incl_len, orig_len) = struct.unpack(endian + 'LLLL', ph)
    cap_time = datetime.datetime.fromtimestamp(ts_sec)
    if (incl_len == orig_len and incl_len <= snaplen and incl_len > 0 ):
        return (ts_sec, ts_usec, incl_len, orig_len, True)
    return (ts_sec, ts_usec, incl_len, orig_len, False)

def check_data(data, filepos, last_time_sec):
    data_len = len(data)
    for i in range(1,(data_len-16)):
        new_data = data[i:i+16]
        (ts_sec2, ts_usec2, incl_len2, orig_len2, check_ok2) = check_packet_header_buff(new_data, last_time_sec, snaplen)
        if (check_ok2):
            cap_time2 = datetime.datetime.fromtimestamp(ts_sec2)
            print("Probably new capture package found inside of data. Check, if the next chunk is also O.K.")
            print("\t\tcounter:%-10s, byte_counter:0x%-6X = %-6s, stime:%s, ts_usec:%-7s, incl_len:0x%-6X = %-6s, orig_len:0x%-6X = %-6s, data:" % (counter,(filepos+i),(filepos+i),cap_time2, ts_usec2, incl_len2, incl_len2, orig_len2, orig_len2))
            nextpos2 = byte_counter+i+incl_len2+24
            if (nextpos+16 > file_to_open_size):
                break # end of file

            (ts_sec3, ts_usec3, incl_len3, orig_len3, check_ok3) = check_packet_header(f, counter, snaplen, nextpos2)
            if (check_ok3):
                f.seek(byte_counter+i)
                print("\t\tThe next chunk is O.K. Set the file pos to probably chunk and continue work...\n")
                return i
            else:
                print("\t\tThe next chunk is not O.K. Continue searching in data...")

    print("")
    return data_len

file_to_open = "F:\\tmp\\290120112105\\capture.cap"
file_to_open_size = os.path.getsize(file_to_open)

f = open(file_to_open, 'rb')
fw = open("F:\\tmp\\290120112105\\capture_write.cap", 'wb')

modified = 0
byte_counter = 0

a = datetime.datetime.fromtimestamp(0)
print(a)

try:
    ph = f.read(4)
    fw.write(ph)

    magic_number, = struct.unpack('<L', ph)
    byte_counter+=4
except:
    logger.error('Seems, there is no valid PCAP file')
    System.exit(1)
if magic_number == 0xa1b2c3d4 or magic_number == 0xa1b2cd34:        # Default or modified libpcap
    # Little endian
    endian = '<'
    if magic_number == 0xa1b2cd34:
        modified = 1
elif magic_number == 0xd4c3b2a1 or magic_number == 0x34cdb2a1:      # Default or modified libpcap
    # Big endian
    endian = '>'
    if magic_number == 0x34cdb2a1:
        modified = 1
else:
    logger.error('Invalid PCAP dump header. Probably not a valid capture file')
    System.exit(1)

# Read the rest of the dumpheader
ph = f.read(20)
fw.write(ph)
(version_major, version_minor, thiszone, sigfigs, snaplen, network) = struct.unpack(endian + 'HHlLLL', ph)
byte_counter+=20

# Loop
counter = 0
check_data_bool = True
ts_sec = -1

while True:

    # Read packet header
    ph = f.read(16)
    if not ph:
        break   # end of file

    (ts_sec, ts_usec, incl_len, orig_len, check_ok) = check_packet_header_buff(ph, ts_sec, snaplen)
    cap_time = datetime.datetime.fromtimestamp(ts_sec)
    printed_line = "counter:%-10s, byte_counter:0x%-6X = %-6s, stime:%s, ts_usec:%-7s, incl_len:0x%-6X = %-6s, orig_len:0x%-6X = %-6s, data:" % (counter,byte_counter,byte_counter,cap_time, ts_usec, incl_len, incl_len, orig_len, orig_len)

    if (check_ok):
        nextpos = byte_counter+incl_len+24
        if (nextpos+16 > file_to_open_size):
            break # end of file

        (ts_sec2, ts_usec2, incl_len2, orig_len2, check_ok2) = check_packet_header(f, counter, snaplen, nextpos)
        cap_time2 = datetime.datetime.fromtimestamp(ts_sec2)
        if (check_ok2):
            byte_counter+=16
            if (counter % 10000 == 0):
                print(printed_line)

            if modified:
                incl_len+=8      # The way it is, don't know, why they had to change this plain old format
            data = f.read(incl_len)
            counter=counter+1
            byte_counter+=incl_len

            fw.write(ph)
            fw.write(data)

            # write data to other file
            continue

        printed_line2 = "counter:%-10s, byte_counter:0x%-6X = %-6s, stime:%s, ts_usec:%-7s, incl_len:0x%-6X = %-6s, orig_len:0x%-6X = %-6s, data:" % (counter,nextpos,nextpos,cap_time2, ts_usec2, incl_len2, incl_len2, orig_len2, orig_len2)

        print("The original is OK, but the next of original seems not to be correct. Go Back...")
        print("\t\t"+printed_line)
        print("\t\t"+printed_line2)
        print("")
        byte_counter+=16 # don't need to repeat checking of the right header
        f.seek(byte_counter)
        continue

    byte_counter+=1
    f.seek(byte_counter)
    print("Analyse the next (1024*1024 Bytes) data  for probably packages...")
    print("\t\t"+printed_line)
    print("")
    data = f.read(1024*1024)
    incl_len = check_data(data, byte_counter, ts_sec)
    byte_counter+=incl_len

fw.close()
f.close()
