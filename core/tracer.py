#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
##################################################################################
# Simple FritzCap python port
# Simplifies generation and examination of traces taken from AVM FritzBox and/or SpeedPort
# Traces can be examined using WireShark
# (c) neil.young 2010 (spongebob.squarepants in http://www.ip-phone-forum.de/)
# based on the Windows GUI exe with same name
##################################################################################
# Copyright (c) 2010, neil.young
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

import urllib.request, urllib.parse, urllib.error, ctypes, platform

from log import Log
from exception_logging_thread import ExceptionLoggingThread

THREAD_SET_INFORMATION = 0x20
THREAD_PRIORITY_ABOVE_NORMAL = 1

''' Tracer runs in a separate thread'''
class Tracer(ExceptionLoggingThread):
    def __init__(self, url, filename):
        self.url = url
        self.i = 0
        self.filename = filename
        ExceptionLoggingThread.__init__(self)

        self.logger = Log().getLogger()

    def monitor(self, n1, n2, n3):
        # n1: running number, n2: chunk size, n3: file size or -1 if unknown
        #print ["|", "/", "-", "\\"][self.i], "\r",
        self.i += 1
        self.i %= 4

    def run_logic(self):
        if platform.system() == "Windows":
            w32 = ctypes.windll.kernel32
            tid = w32.GetCurrentThreadId()
            # Raise thread priority
            handle = w32.OpenThread(THREAD_SET_INFORMATION, False, tid)
            result = w32.SetThreadPriority(handle, THREAD_PRIORITY_ABOVE_NORMAL)
            w32.CloseHandle(handle)
        try:
            self.logger.debug("Trace started  (url:'%s', filename:'%s')" % (self.url, self.filename))
            urllib.request.urlretrieve(self.url, self.filename, self.monitor)
            self.logger.debug("Trace finished (url:'%s', filename:'%s')" % (self.url, self.filename))
        except:
            self.logger.debug("Could not open Trace (url:'%s', filename:'%s')" % (self.url, self.filename))
