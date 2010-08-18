#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
################################################################################# 
# Simple FritzCap python port
# Simplifies generation and examination of traces taken from AVM FritzBox and/or SpeedPort
# Traces can be examined using WireShark
# (c) neil.young 2010 (spongebob.squarepants in http://www.ip-phone-forum.de/)
# based on the Windows GUI exe with same name
##################################################################################
 
import urllib, re, timeit, hashlib, sys, datetime, os

sys.path.append('core')

from tracer import Tracer
from pcap_parse import PcapParser
from g711_decoder import G711Decoder

# Configuration (just change here) ###############################################
boxname         = 'speedport.ip'        # or ip (also fritz.box)
password        = 'yourpassword'        # your password, adapt
protocol        = 'https'               # or http
capfolder       = 'captures'            # plus subfolders according to day, month, year, hour, minute
capfile         = 'capture.cap'         # name of capture file
login_required  = True                  # set to 0 if no login is required
##################################################################################

# Commands
default_login   = 'getpage=../html/de/menus/menu2.html&errorpage=../html/index.html&var:lang=de&var:pagename=home&var:menu=home&=&login:command/password=%s'
sid_challenge   = 'getpage=../html/login_sid.xml'
sid_login       = 'login:command/response=%s&getpage=../html/login_sid.xml'
start           = '?start=1&start1=Start'
stop            = '?stop=1&stop1=Stop'


# Main work horse G.711 extraction/mix
def runparser():
    g711 = G711Decoder(capfile, mix=1, linearize=1)
    PcapParser(capfile, g711.decode).parse()
    g711.finalize()
    
# Main
def main():

    global capfile

    capture = True            # Audio debug shortcut
    extract_audio = True      # Extract audio if available
    
    SID = ''                  # Required later                 
    
    if capture:
        
        # Attempt to login
        if login_required:
    
            try:
                # Try to get a session id SID
                sid = urllib.urlopen(protocol + '://' +  boxname + '/cgi-bin/webcm?' + sid_challenge)
                if sid.getcode() == 200:          
                    # Read and parse the response in order to get the challenge (not a full blown xml parser)
                    challenge = re.search('<Challenge>(.*?)</Challenge>', sid.read()).group(1)
                    
                    # Create a UTF-16LE string from challenge + '-' + password, non ISO-8859-1 characters will except here (e.g. EUR)
                    challenge_bf = (challenge + '-' + password).decode('iso-8859-1').encode('utf-16le')
                    
                    # Calculate the MD5 hash
                    m = hashlib.md5()
                    m.update(challenge_bf)
            
                    # Make a byte response string from challenge + '-' + md5_hex_value 
                    response_bf = challenge + '-' + m.hexdigest().lower()
                    
                    # Answer the challenge
                    login = urllib.urlopen(protocol + '://' + boxname + '/cgi-bin/webcm', sid_login % response_bf)

                    if login.getcode() == 200:
                        SID = re.search('<SID>(.*?)</SID>', login.read()).group(1)
                        print "Login OK, SID %s" % SID
                    else:
                        print "Could not login"
                        return
            except:
                # Legacy login
                command = urllib.urlopen(protocol + '://' + boxname + '/cgi-bin/webcm', default_login % password)
                response = command.read()
                # Right now I don't know how to check the result of a login operation. So I just search for the errorMessage
                if command.getcode() == 200:
                    try:
                        result = urllib.unquote(re.search('<p class="errorMessage">(.*?)</p>', response).group(1).decode('iso-8859-1')).replace("&nbsp;"," ")
                    except:
                        result = ''
                    print 'Login attempt was made. %s' % result
                    
    
        # Create capfile folder
        folder = capfolder + '/' + (datetime.datetime.now().strftime('%d%m%Y%H%M'))
        capfile = folder + '/' + capfile
        if not os.path.exists(folder):
            os.makedirs(folder)
          
        # Start tracer thread, wait for console input to stop
        if SID != '':
            Tracer(protocol + '://' + boxname + '/cgi-bin/capture_notimeout' + start + "&sid=%s" % SID, capfile).start()
        else:
            Tracer(protocol + '://' + boxname + '/cgi-bin/capture_notimeout' + start, capfile).start()
            
        print 'Trace started, abandon with <ENTER>'
        raw_input()
        # Clean stop
        print 'Stopping trace'
        if SID != '':
            urllib.urlopen(protocol + '://' + boxname + '/cgi-bin/capture_notimeout' + stop)
        else:
            urllib.urlopen(protocol + '://' + boxname + '/cgi-bin/capture_notimeout' + stop + "&sid=%s" % SID)
        print 'Capture done'
    
    # Parse the captured file
    if extract_audio:
        print 'Extracting audio...'
        print timeit.Timer('runparser()', 'from __main__ import runparser').timeit(number=1), "seconds"
#       runparser()
    print 'All done'
          
if __name__ == '__main__': 
    main()  
