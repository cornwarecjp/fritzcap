#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
##################################################################################
# Simple FritzCap python port
# Simplifies generation and examination of traces taken from AVM FritzBox and/or SpeedPort
# Traces can be examined using WireShark
# (c) neil.young 2010 (spongebob.squarepants in http://www.ip-phone-forum.de/)
# based on the Windows GUI exe with same name
##################################################################################


debug = True

''' Capable of logging up to 15 arguments'''
def log(*args):
    if debug:
        print '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'[:3*len(args)] % args        
    