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


import threading
import queue
import time, random
import telnetlib
import datetime

from log import Log
from capture_monitor import CaptureMonitor
from exception_logging_thread import ExceptionLoggingThread

class CallMonitor(ExceptionLoggingThread):

    def __init__(self, capture_monitor, box_name, call_service_port):
        ExceptionLoggingThread.__init__(self)
        self._stop = threading.Event()

        self.capture_monitor = capture_monitor
        self.box_name = box_name
        self.call_service_port = call_service_port

        self.logger = Log().getLogger()

        self.logger.debug("CallMonitor(capture_monitor:'%s', box_name:'%s', call_service_port:'%s')." % (capture_monitor,box_name,call_service_port))

    def init_connection(self):
        # Connect to the call monitor service over telnet.
        self.logger.info("Connect    to the call monitor service on %s:%s." % (self.box_name,self.call_service_port))

        try:
            self.tn = telnetlib.Telnet(self.box_name, self.call_service_port)
        except IOError:
            self.logger.error("Cannot create connection to the call monitor service on %s:%s." % (self.box_name,self.call_service_port))
            self.tn = None
            return

        self.logger.info("Connected  to the call monitor service on %s:%s." % (self.box_name,self.call_service_port))

    def run_logic(self):
        self.logger.debug("Thread started.")
        callers_count = 0                     # Set the count of currently led calls to 0.
        call_id_map = {}
        self.init_connection()
        while self.tn and not self._stop.isSet():
            self.logger.debug("Wait for call monitor status change.")
            line = ""
            while (not self._stop.isSet() and not line.endswith("\n")):
                try:
                    line = line + self.tn.read_until("\n", timeout=5)        # Wait until one line data was readed from the telnet connection.
                except AttributeError:
                        self.logger.error("Cannot read input data from telnet service. Maybe the telnet connection is broken. Stop the service.")
                        self._stop.set()

                if (self._stop.isSet() and self.tn):
                    self.logger.debug("Close the connection to the telnet session.")
                    self.tn.close()
                    self.logger.debug("Close the connection to the telnet session finished.")
                    self.tn = None
                    self.logger.info("Connection to the call monitor service on %s:%s stopped." % (self.box_name,self.call_service_port))
                    continue

            if (self._stop.isSet()):
                break

            line = line.strip()
            if (not line):
                continue

            sline = line.split(";")

            event_time = datetime.datetime.now()
            # parse the original telnet time. Example: 13.01.11 21:48:31
            original_event_time = time.strptime(sline[0], "%d.%m.%y %H:%M:%S") # 13.01.11 21:48:31

            self.logger.debug("Telnet:'"+line+"'")

            # get the event command
            command = sline[1]

            if command == "RING":             # It rings, an incoming call.
                callers_count += 1            # Increase the count of currently led calls.
                call_partner = sline[3]
                if not call_partner:
                    call_partner = "Unknown"
                me = sline[4]
                if not me:
                    me = "Unknown"

                if (self.capture_monitor is None):
                    me_numbername = me
                    callpartner_numbername = call_partner

                else:
                    self.capture_monitor.set_data("callevent.name", command)
                    self.capture_monitor.set_data("acalls.number", callers_count)
                    self.capture_monitor.set_data("lineport.name", sline[5])

                    self.capture_monitor.set_data("tocall", original_event_time)
                    self.capture_monitor.set_data("tcall", event_time)
                    self.capture_monitor.set_callnumber("caller", call_partner)
                    self.capture_monitor.set_callnumber("dialed", me)
                    self.capture_monitor.set_callnumber("me", me)
                    self.capture_monitor.set_callnumber("callpartner", call_partner)

                    me_numbername = self.capture_monitor.get_call_numbername(me)
                    callpartner_numbername = self.capture_monitor.get_call_numbername(call_partner)

                self.logger.info("Ring       (ID:%s, ActiveCalls.:%s, Caller:%s, DialedNumber:%s, LinePort:%s)" % (sline[2],callers_count,callpartner_numbername,me_numbername,sline[5]))
                call_id_map[sline[2]] = [callpartner_numbername,me_numbername,sline[5]]


            elif command == "CALL":           # Number is dialed, an outgoing call.
                callers_count += 1            # Increase the count of currently led calls.

                me = sline[4]
                if not me:
                    me = "Unknown"
                call_partner = sline[5]
                if not call_partner:
                    call_partner = "Unknown"

                if (self.capture_monitor is None):
                    me_numbername = self.capture_monitor.get_call_numbername(me)
                    callpartner_numbername = self.capture_monitor.get_call_numbername(call_partner)
                else:
                    self.capture_monitor.set_data("callevent.name", command)
                    self.capture_monitor.set_data("acalls.number", callers_count)
                    self.capture_monitor.set_data("lineport.name", sline[6])
                    self.capture_monitor.set_data("tocall", original_event_time)
                    self.capture_monitor.set_data("tcall", event_time)
                    self.capture_monitor.set_callnumber("caller", me)
                    self.capture_monitor.set_callnumber("dialed", call_partner)
                    self.capture_monitor.set_callnumber("me", me)
                    self.capture_monitor.set_callnumber("callpartner", call_partner)

                    me_numbername = self.capture_monitor.get_call_numbername(me)
                    callpartner_numbername = self.capture_monitor.get_call_numbername(call_partner)

                self.logger.info("Call       (ID:%s, ActiveCalls.:%s, Caller:%s, DialedNumber:%s, LinePort:%s)" % (sline[2],callers_count,me_numbername,callpartner_numbername,sline[6]))
                call_id_map[sline[2]] = [me_numbername,callpartner_numbername,sline[6]]
            elif command == "CONNECT":        # Conversation started.
                if (self.capture_monitor is not None):
                    self.capture_monitor.set_data("toconn", original_event_time)
                    self.capture_monitor.set_data("tconn", event_time)
                self.logger.info("Connect    (ID:%s, ActiveCalls.:%s, Caller:%s, DialedNumber:%s, LinePort:%s)" % (sline[2],callers_count,call_id_map[sline[2]][0],call_id_map[sline[2]][1],call_id_map[sline[2]][2]))
                continue                      # Don't increase currently led calls, because already done with CALL/RING.
            elif command == "DISCONNECT":     # Call was ended.
                callers_count -= 1            # Decrease the count of currently led calls.

                if (self.capture_monitor is not None):
                    self.capture_monitor.set_data("todisc", original_event_time)
                    self.capture_monitor.set_data("tdisc", event_time)
                    self.capture_monitor.set_data("acalls.number", callers_count)

                self.logger.info("Disconnect (ID:%s, ActiveCalls.:%s, Caller:%s, DialedNumber:%s, LinePort:%s)" % (sline[2],callers_count,call_id_map[sline[2]][0],call_id_map[sline[2]][1],call_id_map[sline[2]][2]))
                if (callers_count < 0):
                    self.logger.warning("There is more stopped calls than started. Data corrupt or program started while calling. Normalize ActiveCalls to '0'")
                    callers_count = 0;
                    if (self.capture_monitor is not None):
                        self.capture_monitor.set_data("acalls.number", callers_count)
            else:
                continue

            if (self.capture_monitor is not None):
                if callers_count == 1:        # There is at least 1 started call, start capture of data.
                    self.logger.debug("There is at least 1 active call. Send start_capture event to the CaptureMonitor.")
                    self.capture_monitor.start_capture();
                elif callers_count == 0:      # there are no more active calls
                    self.logger.debug("There is no more active calls. Send stop_capture event to the CaptureMonitor.")
                    self.capture_monitor.stop_capture();

        self._stop.set()
        if (self.capture_monitor is not None):
            self.capture_monitor.stop()
        self.logger.debug("Thread stopped.")

    def stop (self):
        self.logger.debug("Received signal to stop the thread.")
        self._stop.set()

    def stopped (self):
        return self._stop.isSet()
