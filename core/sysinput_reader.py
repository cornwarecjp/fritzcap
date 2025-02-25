#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#################################################################################
# Simple FritzCap python port
# Simplifies generation and examination of traces taken from AVM FritzBox and/or SpeedPort
# Traces can be examined using WireShark
# (c) tom2bor 2011 (tom2bor in http://www.ip-phone-forum.de/)
# based on the Windows GUI exe with same name
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


import sys
import threading
import queue
import time, random

import logging
from log import Log
from exception_logging_thread import ExceptionLoggingThread

class SytemInputFileReader(ExceptionLoggingThread):

    def __init__(self, decode_work_queue):
        ExceptionLoggingThread.__init__(self)
        self._stop = threading.Event()
        self.decode_work_queue = decode_work_queue

        self.logger = Log().getLogger()
        self.logger.debug("SytemInputFileReader(decode_work_queue:'%s')" % (decode_work_queue))

    def run_logic(self):
        self.logger.debug("Thread started.")
        for line in sys.stdin:
            line = line.strip()
            if (line):
                self.logger.debug("Got new file to decode from system.in. Add '%s' to the decode work queue." % (line))
                self.decode_work_queue.put(line)

        self.logger.debug("Put the last None element to the queue.")
        self.decode_work_queue.put(None)

        self._stop.set()
        self.logger.debug("Thread stopped.")

    def stop (self):
        self._stop.set()
        sys.stdin.flush()

    def stopped (self):
        return self._stop.isSet()
