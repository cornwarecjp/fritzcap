##################################################################################
# Simple FritzCap python port
# Simplifies generation and examination of traces taken from AVM FritzBox and/or SpeedPort
# Traces can be examined using WireShark
# (c) neil.young 2010 (spongebob.squarepants in http://www.ip-phone-forum.de/)
# based on the Windows GUI exe with same name#
##################################################################################
 
import urllib, threading, sys

# Configuration (just change here) ###############################################
boxname = 'speedport.ip'                # or ip (also fritz.box)
password = 'yourpassword'               # your password, adapt
protocol = 'https'                      # or http
capfile = 'test.cap'                    # name of capture file
login_required = 1                      # set to 0 if no login is required
##################################################################################

# Commands
login = 'getpage=../html/de/menus/menu2.html&errorpage=../html/index.html&var:lang=de&var:pagename=home&var:menu=home&=&login:command/password=%s'
start = '?start=1&start1=Start'
stop =  '?stop=1&stop1=Stop'

# Tracer runs in a separate thread
class TraceGetter(threading.Thread):
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
        try:
            urllib.urlretrieve(self.url, self.filename, self.monitor)
            print "Trace stopped"
        except:
            print "Could not open %s" % self.url

# Main
def main():
    # Attempt to login
    if login_required:
        command = urllib.urlopen(protocol + '://' + boxname + '/cgi-bin/webcm', login % password)
        response = command.read()
        print 'Login', response

    # Start tracer thread, wait for console input to stop
    thread = TraceGetter(protocol + '://' + boxname + '/cgi-bin/capture_notimeout' + start, capfile)
    thread.start()
    print "Trace started, stop with <ENTER>"
    raw_input()
    # Clean stop
    print "Stopping trace"
    urllib.urlopen(protocol + '://' + boxname + '/cgi-bin/capture_notimeout' + stop)
    print "Capture done"

if __name__ == "__main__": 
    main()  
