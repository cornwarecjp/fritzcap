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
from pcap_parse import PcapParser
from g711_decoder import G711Decoder
from exception_logging_thread import ExceptionLoggingThread

class CapfileWorker(ExceptionLoggingThread):

    def __init__(self, worker_id, decode_work_queue):
        ExceptionLoggingThread.__init__(self)
        self.decode_work_queue = decode_work_queue
        self.worker_id = worker_id
        self._stop = threading.Event()

        self.logger = Log().getLogger()
        self.logger.debug("CapfileWorker(worker_id:%s, decode_work_queue:%s)." % (worker_id, decode_work_queue))

    def run_logic(self):
        self.logger.debug("Thread started.")
        while not self._stop.isSet():
            try:
                filename = self.decode_work_queue.get()
                if (filename is None):
                    self.logger.debug("Became None element, put a None element to the queue for the others workers and break the work.")
                    self.decode_work_queue.put(None)
                    break

                self.process(filename)
            finally:
                self.decode_work_queue.task_done()

        self._stop.set()
        self.logger.debug("Thread stopped.")

    def process(self, filename):
        self.logger.info("Decode process started  (worker_id:%s, file:'%s')" % (self.worker_id,filename))
        g711 = G711Decoder(filename, mix=1, linearize=1)
        PcapParser(filename, g711.decode).parse()
        g711.finalize()
        self.logger.info("Decode process finished (worker_id:%s, file:'%s')" % (self.worker_id,filename))

    def stop (self):
        self.logger.debug("Received signal to stop the thread.")
        self._stop.set()
        self.decode_work_queue.put(None)

    def stopped (self):
        return self._stop.isSet()
