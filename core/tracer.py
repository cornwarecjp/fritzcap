#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
##################################################################################
# Simple FritzCap python port
# Simplifies generation and examination of traces taken from AVM FritzBox and/or SpeedPort
# Traces can be examined using WireShark
# (c) neil.young 2010 (spongebob.squarepants in http://www.ip-phone-forum.de/)
# based on the Windows GUI exe with same name
##################################################################################

import threading, urllib, ctypes, platform
import util

THREAD_SET_INFORMATION = 0x20
THREAD_PRIORITY_ABOVE_NORMAL = 1


''' Tracer runs in a separate thread'''
class Tracer(threading.Thread):
    def __init__(self, url, filename):
        self.url = url
        self.i = 0
        self.filename = filename
        threading.Thread.__init__(self)
 
    def monitor(self, n1, n2, n3):
        # n1: running number, n2: chunk size, n3: file size or -1 if unknown
        print ["|", "/", "-", "\\"][self.i], "\r",
        self.i += 1
        self.i %= 4
                
    def run(self):
        if platform.system() == "Windows":
            w32 = ctypes.windll.kernel32
            tid = w32.GetCurrentThreadId()
            # Raise thread priority
            handle = w32.OpenThread(THREAD_SET_INFORMATION, False, tid)
            result = w32.SetThreadPriority(handle, THREAD_PRIORITY_ABOVE_NORMAL)
            w32.CloseHandle(handle)
        try:
            urllib.urlretrieve(self.url, self.filename, self.monitor)
            util.log('Trace finished server side')
        except:
            util.log('Could not open %s' % self.url)


    