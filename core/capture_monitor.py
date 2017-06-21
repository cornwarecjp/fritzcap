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

import datetime
import logging
import threading
import Queue
import time, datetime, random
import urllib
import os
import re
import hashlib

from log import Log
from string_helper import StringHelper
from tracer import Tracer

class CaptureMonitor(threading.Thread):

    state_started = False
    next_stop_time = 0
    next_start_time = 0
    cap_file_path = ""

    def __init__(self, decode_work_queue, data_map, box_name, password, protocol, cap_folder, cap_file, login_required, default_login, sid_challenge, sid_login, start_str, stop_str, after_capture_time):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

        self.decode_work_queue = decode_work_queue
        self.data_map = data_map
        self.box_name = box_name
        self.password = password
        self.protocol = protocol
        self.cap_folder = cap_folder
        self.cap_file = cap_file
        self.login_required = login_required
        self.default_login = default_login
        self.sid_challenge = sid_challenge
        self.sid_login = sid_login
        self.start_str = start_str
        self.stop_str = stop_str
        self.after_capture_time = after_capture_time
        self.SID = ''

        self.wait_condition = threading.Condition()

        self.logger = Log().getLogger()
        self.logger.debug("CaptureMonitor(decode_work_queue:'%s', data_map:'%s', box_name:'%s', password:'%s', protocol:'%s', cap_folder:'%s', cap_file:'%s', login_required:'%s', default_login:'%s', sid_challenge:'%s', sid_login:'%s', start_str:'%s', stop_str:'%s', after_capture_time:'%s')" % (decode_work_queue,data_map,box_name,password,protocol,cap_folder,cap_file,login_required,default_login,sid_challenge,sid_login,start_str,stop_str,after_capture_time))

    def run(self):
        self.logger.debug("Thread started.")

        if self.login_required:
           if (not self.init_login()):
               self.logger.debug("Could not login. Stop the capture thread.")
               self._stop.set()

        while not self._stop.isSet():
            ###################
            ### pre_capture ###
            ###################
            # Wait until start_capture coomand was started...
            self.logger.debug("pre_capture acquire lock.")
            self.wait_condition.acquire()
            self.logger.debug("pre_capture acquire lock finished.")
            while not self._stop.isSet() and (self.state_started == False or self.next_start_time > time.time()):
                if self.next_start_time > time.time():
                    waittime = self.next_start_time - time.time()
                    if (self.logger.isEnabledFor(logging.DEBUG)):
                        self.logger.debug("pre_capture wait(%f)." % (waittime))
                    self.wait_condition.wait(waittime)
                    if (self.logger.isEnabledFor(logging.DEBUG)):
                        self.logger.debug("pre_capture wait(%f) finished." % (waittime))
                else:
                    if (self.logger.isEnabledFor(logging.DEBUG)):
                        self.logger.debug("pre_capture wait().")
                    self.wait_condition.wait()
                    if (self.logger.isEnabledFor(logging.DEBUG)):
                        self.logger.debug("pre_capture wait() finished.")

            self.logger.debug("pre_capture release lock.")
            self.wait_condition.release()
            self.logger.debug("pre_capture release lock finished.")

            if (self._stop.isSet()):
                logging.debug("The capture was not started. Not need to stop the capture. Can stop immediately.")
                break

            self.sub_start_capture()

            ####################
            ### post_capture ###
            ####################
            # Wait until stop_capture command was started...
            self.logger.debug("post_capture acquire lock.")
            self.wait_condition.acquire()
            self.logger.debug("post_capture acquire lock finished.")
            while not self._stop.isSet() and (self.state_started == True or self.next_stop_time > time.time()):
                if self.next_stop_time > time.time():
                    waittime = self.next_stop_time - time.time()
                    if (self.logger.isEnabledFor(logging.DEBUG)):
                        self.logger.debug("post_capture wait(%f)." % (waittime))
                    self.wait_condition.wait(waittime)
                    if (self.logger.isEnabledFor(logging.DEBUG)):
                        self.logger.debug("post_capture wait(%f) finished." % (waittime))
                else:
                    if (self.logger.isEnabledFor(logging.DEBUG)):
                        self.logger.debug("post_capture wait().")
                    self.wait_condition.wait()
                    if (self.logger.isEnabledFor(logging.DEBUG)):
                        self.logger.debug("post_capture wait() finished.")
            self.logger.debug("post_capture release lock.")
            self.wait_condition.release()
            self.logger.debug("post_capture release lock finished.")

            self.sub_stop_capture()

        if (self._stop.isSet()):
            if (self.decode_work_queue is not None):
                self.decode_work_queue.put(None)
        else:
            self._stop.set()
        self.logger.debug("Thread stopped.")



    def init_login(self):
        try:
            self.logger.debug("Login attempt to the the FritzBox (box_name:%s)" % (self.box_name))

            # Try to get a session id SID
            conn_url = self.protocol + '://' + self.box_name + '/login_sid.lua'
            self.logger.debug("Call the challange token url (url:'%s')" % conn_url)
            self.sid = urllib.urlopen(conn_url)
            if self.sid.getcode() == 200:
                # Read and parse the response in order to get the challenge (not a full blown xml parser)
                readed_chalange_str = self.sid.read()
                challenge = re.search('<Challenge>(.*?)</Challenge>', readed_chalange_str).group(1)

                # Create a UTF-16LE string from challenge + '-' + password, non ISO-8859-1 characters will except here (e.g. EUR)
                challenge_bf = (challenge + '-' + self.password).decode('iso-8859-1').encode('utf-16le')

                # Calculate the MD5 hash
                m = hashlib.md5()
                m.update(challenge_bf)

                # Make a byte response string from challenge + '-' + md5_hex_value
                response_bf = challenge + '-' + m.hexdigest().lower()

                # Answer the challenge
                conn_url = self.protocol + '://' + self.box_name + '/login_sid.lua?username=root&response=' + response_bf
                self.logger.debug("Call the read seed token url (url:'%s', data:'%s')." % (conn_url,self.sid_login % response_bf))
                login = urllib.urlopen(conn_url)

                if login.getcode() == 200:
                    readed_login_str = login.read()
                    self.SID = re.search('<SID>(.*?)</SID>', readed_login_str).group(1)
                    if (self.SID == '0000000000000000'):
                        self.logger.error("Could not login to the FritzBox: Not authorized.")
                    else:
                        self.logger.debug("Login OK (SID: %s)" % self.SID)
                    return True

                else:
                    self.logger.error("Could not login to the FritzBox: Unknown error")
            else:
                self.logger.error("Could not login to the FritzBox: Error 404.")
        except:
            # Legacy login
            command = urllib.urlopen(self.protocol + '://' + self.box_name + '/cgi-bin/webcm', self.default_login % self.password)
            response = command.read()
            # Right now I don't know how to check the result of a login operation. So I just search for the errorMessage
            if command.getcode() == 200:
                try:
                    result = urllib.unquote(re.search('<p class="errorMessage">(.*?)</p>', response).group(1).decode('iso-8859-1')).replace("&nbsp;"," ")
                except:
                    result = ''
                self.logger.error('Login attempt was made, but something was wrong: %s' % result)
        return False

    def init_capture_file(self):
        # Create capfile folder
        folder = StringHelper.parse_string(self.cap_folder, self.data_map)
        folder = folder.replace("\\","/")
        if (not folder.endswith("/")):
            folder = folder+"/"

        file = StringHelper.parse_string(self.cap_file, self.data_map)

        self.cap_file_path = folder+file
        self.logger.debug("Initialize capture file (folder:%s, file:%s)." % (folder,file))
        if not os.path.exists(folder):
            self.logger.debug("Destination folder:'%s' not exists. Create." % folder)
            os.makedirs(folder)

    def sub_start_capture(self):
        # Start tracer thread, wait for console input to stop
        if self.login_required and not self.init_login():
            self.logger.debug("Could not login. Stop the capture thread.")
            self._stop.set()
            return

        self.set_data("tcaps",datetime.datetime.now())
        self.logger.debug("data_map:%s" % (self.data_map))
        self.init_capture_file()
        self.logger.info("Start capture (capture_file:'%s')." % (self.cap_file_path))
        if self.SID != '':
            url = self.protocol + '://' + self.box_name + '/cgi-bin/capture_notimeout' + self.start_str + "&sid=%s" % self.SID
        else:
            url = self.protocol + '://' + self.box_name + '/cgi-bin/capture_notimeout' + self.start_str

        self.logger.debug("Send capture start request to the box          (url:'%s', capture_file:'%s')." % (url, self.cap_file_path))
        Tracer(url, self.cap_file_path).start()
        self.logger.debug("Send capture start request to the box finished (url:'%s', capture_file:'%s')." % (url, self.cap_file_path))

    def sub_stop_capture(self):
        # Clean stop
        if self.login_required and not self.init_login():
            self.logger.debug("Could not login. Stop the capture thread.")
            self._stop.set()
            return

        if self.SID != '':
            url = self.protocol + '://' + self.box_name + '/cgi-bin/capture_notimeout' + self.stop_str + "&sid=%s" % self.SID
        else:
            url = self.protocol + '://' + self.box_name + '/cgi-bin/capture_notimeout' + self.stop_str
        self.logger.debug("Send capture stop request to the box           (url:'%s', capture_file:'%s')." % (url, self.cap_file_path))
        urllib.urlopen(url)
        self.logger.debug("Send capture stop request to the box finished  (url:'%s', capture_file:'%s')." % (url, self.cap_file_path))
        self.logger.info("Capture finished (capture_file:'%s')." % (self.cap_file_path))
        self.set_data("tcape",datetime.datetime.now())

        if (self.decode_work_queue is not None):
            self.logger.debug("Add captured file '%s' to the decoding work queue." % (self.cap_file_path))
            self.decode_work_queue.put(self.cap_file_path)

    def start_capture(self):
        self.wait_condition.acquire()
        self.logger.debug("start_capture called.")
        self.state_started = True
        self.wait_condition.notify_all()
        self.wait_condition.release()

    def stop_capture(self):
        self.wait_condition.acquire()
        self.logger.debug("stop_capture called.")
        self.state_started = False
        if self.after_capture_time > 0:
            self.next_stop_time = time.time() + self.after_capture_time
        self.wait_condition.notify_all()
        self.wait_condition.release()


    def stop (self):
        self.logger.debug("Received signal to stop the thread.")
        self._stop.set()
        self.wait_condition.acquire()
        if self.after_capture_time > 0:
            self.next_stop_time = time.time() + self.after_capture_time
        self.wait_condition.notify_all()
        self.wait_condition.release()

    def stopped (self):
        return self._stop.isSet()

    def set_callnumber(self, key, number):
        self.data_map[key+".number"] = number
        self.data_map[key+".name"] = ""
        self.data_map[key+".numbername"] = number
        if (self.data_map.has_key("pbook_number."+number)):
            self.data_map[key+".name"] = self.data_map.get("pbook_number."+number)
            self.data_map[key+".numbername"] = self.get_call_numbername(number)

    def get_call_numbername(self, number):
        if (not number):
            number = "Unknown"

        if (self.data_map.has_key("pbook_number."+number)):
            return number+"("+self.data_map.get("pbook_number."+number)+")"
        return number

    def set_data(self, key, value):
        self.data_map[key]=value
