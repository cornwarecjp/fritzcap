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
import re

import logging
from log import Log

class StringHelper():

    # tstart: time of program start
    # tcall: time of ring/call (_Y: year)
    # tconn: time of connection
    # tdisc: time of disconnection
    # tcaps: time of starting capture
    # tcape: time of ending capture
    # caller: the caller numer/name (id,nr,name,)
    # dialed: the dialed number/name
    # me:      my number/name
    # callpartner: foreign/calling partner number/name
    # acalls: active calls number
    # lineport: the used line port name (SIP0,SIP1,etc.)


    def __init__(self):
        self.logger = Log().getLogger()
        self.logger.debug("StringHelper()")

    def parse_string(data_str, data_map):
        datetime_parse_str = ""
        for (key, value) in list(data_map.items()):
            if (type(value) == datetime.datetime):
                datetime_parse_str = datetime_parse_str + "|" + key

        datetime_parse_str = datetime_parse_str[1:]
#        compile_str = r"(%\((tstart).(\w+)\))"
#        pattern = re.compile(compile_str)

        compile_str = r"(%\((" + datetime_parse_str + r")\.(.+)\))"
        pattern = re.compile(compile_str)
        matchObj = pattern.search(data_str)
        while (matchObj):
            value = StringHelper.parse_dates(matchObj.group(2), matchObj.group(3), data_map)
            data_str = data_str[:matchObj.start(1)]+value+data_str[matchObj.end(1):]
            matchObj = pattern.search(data_str)

        compile_str = r"(%\(((\w+).(\w+))\))"
        pattern = re.compile(compile_str)
        matchObj = pattern.search(data_str)
        while (matchObj):
            data_key = matchObj.group(2)
            if (data_key in data_map):
                value = data_map.get(data_key)
            else:
                value = ""
            data_str = data_str[:matchObj.start(1)]+value+data_str[matchObj.end(1):]
            matchObj = pattern.search(data_str)

        return data_str

    def parse_dates(time_type, time_format, data_map):
        work_time = datetime.date(1900,1,1)
        if (time_type in data_map):
            work_time = data_map.get(time_type)

        time_format = re.sub(r"(\w)", r"%\1", time_format)
        str = (work_time.strftime(time_format))
        return str

    parse_string = staticmethod(parse_string)
    parse_dates = staticmethod(parse_dates)
