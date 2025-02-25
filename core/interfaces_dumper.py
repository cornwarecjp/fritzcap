#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#################################################################################
# Dumps the Fritz!Box interfaces by parsing http://fritz.box/html/capture.html
# Based on CaptureMonitor.py
# (c) wiert.me 2017 (https://wiert.me)
##################################################################################
# Copyright (c) 2017, wiert.me
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
import queue
import time, datetime, random
import urllib.request, urllib.parse, urllib.error
import os
import re
import hashlib

from log import Log
from string_helper import StringHelper
from tracer import Tracer

from html.parser import HTMLParser
from html.entities import name2codepoint
from exception_logging_thread import ExceptionLoggingThread

## https://docs.python.org/2/library/htmlparser.html
class CaptureLuaHtmlParser(HTMLParser):
    # Extract data from html fragments like these:
    # <th>1. Internet connection</th>
    # <td class="buttonrow">
    # <button type="submit" name="start" id="uiStart_1" value="2-1">Start</button>
    # </td>
    # <th>eth3</th>
    # <td class="buttonrow">
    # <button type="submit" name="start" id="uiStart_eth3" value="1-eth3">Start</button>
    # </td>
    # Future enhancement: also take into account the <h3> headers.

    def __init__(self):
        HTMLParser.__init__(self)
        self.last_end_tag = ""
        self.last_start_tag = ""
        self.last_th_data = ""
        self.data = [] # output list of (key,value) pairs
        self.recording = 0

    ## https://stackoverflow.com/questions/16773583/python-extracting-specific-data-with-html-parser
    def handle_starttag(self, tag, attrs):
        # print "Start tag:", tag
        self.last_start_tag = tag
        if tag != 'button':
            return
        button_attribute_type_submit = False
        button_attribute_name_start = False
        for name, value in attrs:
            # print "    attr: %s=%s; th=%s" % (name, value, self.last_th_data)
            if (name == 'type') and (value == 'submit'):
                button_attribute_type_submit = True
            if button_attribute_type_submit and (name == 'name') and (value == 'start'):
                button_attribute_name_start = True
            if button_attribute_type_submit and button_attribute_name_start and (name == 'value'):
                # print "    button: type=submit, name=start, value=%s; th=%s" % (value, self.last_th_data)
                ## https://stackoverflow.com/questions/3276040/how-can-i-use-the-python-htmlparser-library-to-extract-data-from-a-specific-div
                self.data.append((value, self.last_th_data)) # (button value value, th content)
        ## https://stackoverflow.com/questions/24251334/return-data-from-htmlparser-handle-starttag

    def handle_endtag(self, tag):
        # print "End tag  :", tag
        self.last_end_tag = tag

    def handle_data(self, data):
        # print "Data     :", data
        if (self.last_start_tag == 'th') and (self.last_end_tag != 'th'):
            self.last_th_data = data

    def handle_comment(self, data):
        # print "Comment  :", data
        pass

    def handle_entityref(self, name):
        # c = unichr(name2codepoint[name])
        # print "Named ent:", c
        pass

    def handle_charref(self, name):
        # if name.startswith('x'):
        #     c = unichr(int(name[1:], 16))
        # else:
        #     c = unichr(int(name))
        # print "Num ent  :", c
        pass

    def handle_decl(self, data):
        # print "Decl     :", data
        pass


class InterfacesDumper(ExceptionLoggingThread):

    def __init__(self, box_name, username, password, protocol, login_required, default_login, sid_challenge, sid_login):
        ExceptionLoggingThread.__init__(self)
        self._stop = threading.Event()

        self.box_name = box_name
        self.username = username
        self.password = password
        self.protocol = protocol
        self.login_required = login_required
        self.default_login = default_login
        self.sid_challenge = sid_challenge
        self.sid_login = sid_login
        self.SID = ''

        self.logger = Log().getLogger()
        self.logger.debug("InterfacesDumper(box_name:'%s', username:'%s', password:'%s', protocol:'%s', login_required:'%s', default_login:'%s', sid_challenge:'%s', sid_login:'%s')" % (box_name,username,password,protocol,login_required,default_login,sid_challenge,sid_login))

    def run_logic(self):
        self.logger.debug("Thread started.")

        if self.login_required:
           if (not self.init_login()):
               self.logger.debug("Could not login. Stop the capture thread.")
               self._stop.set()


        if self.SID != '':
            url = self.protocol + '://' + self.box_name + '/capture.lua' + "?sid=%s" % self.SID
        else:
            url = self.protocol + '://' + self.box_name + '/capture.lua'
        ## https://docs.python.org/2/library/urllib.html
        url_handle = urllib.request.urlopen(url)
        html_content = url_handle.read()
        # self.logger.debug("%s" % html_content)
        parser = CaptureLuaHtmlParser()
        parser.feed(html_content)
        # print parser.data
        self.logger.info("Fritz!Box interfaces from %s: key = value" % url)
        keyValuePairs = sorted(parser.data)
        for (key, value) in keyValuePairs:
            ## https://stackoverflow.com/questions/10623727/python-spacing-and-aligning-strings
            self.logger.info("  %-*s= %s" % (20,key, value))

        self._stop.set()
        self.logger.debug("Thread stopped.")

    def init_login(self):
        try:
            self.logger.debug("Login attempt to the the FritzBox (box_name:%s)" % (self.box_name))

            # Try to get a session id SID
            conn_url = self.protocol + '://' + self.box_name + '/login_sid.lua'
            self.logger.debug("Call the challange token url (url:'%s')" % conn_url)
            self.sid = urllib.request.urlopen(conn_url)
            sid_http_result = self.sid.getcode()
            self.logger.debug("SID HTTP result:%s" % sid_http_result)
            if sid_http_result == 200:
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
                conn_url = self.protocol + '://' + self.box_name + '/login_sid.lua?username=' + self.username + '&response=' + response_bf
                self.logger.debug("Call the read seed token url (url:'%s', data:'%s')." % (conn_url,self.sid_login % response_bf))
                login = urllib.request.urlopen(conn_url)
                login_http_result = login.getcode()
                self.logger.debug("Login HTTP result:%s" % login_http_result)
                if login_http_result == 200:
                    read_login_str = login.read()
                    self.SID = re.search('<SID>(.*?)</SID>', read_login_str).group(1)
                    if (self.SID == '0000000000000000'):
                        self.logger.error("Could not login to the FritzBox: Not authorized.  (SID: %s)" % self.SID)
                    else:
                        self.logger.debug("Login OK (SID: %s)" % self.SID)
                    return True

                else:
                    self.logger.error("Could not login to the FritzBox: Unknown error")
            else:
                self.logger.error("Could not login to the FritzBox: Error 404.")
        except Exception as e:
            self.logger.debug("Exception during SID logon: %s" % e )
            # Legacy login
            command = urllib.request.urlopen(self.protocol + '://' + self.box_name + '/cgi-bin/webcm', self.default_login % self.password)
            response = command.read()
            # Right now I don't know how to check the result of a login operation. So I just search for the errorMessage
            if command.getcode() == 200:
                try:
                    result = urllib.parse.unquote(re.search('<p class="errorMessage">(.*?)</p>', response).group(1).decode('iso-8859-1')).replace("&nbsp;"," ")
                except:
                    result = ''
                self.logger.error('Login attempt was made, but something was wrong: %s' % result)
        return False

    def stop (self):
        self.logger.debug("Received signal to stop the thread.")
        self._stop.set()

    def stopped (self):
        return self._stop.isSet()
