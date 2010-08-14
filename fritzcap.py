# Simple FritzCap python port
# Simplifies generation and examination of traces taken from AVM FritzBox and/or SpeedPort
# Traces can be examined using WireShark
# (c) neil.young 2010 (spongebob.squarepants in http://www.ip-phone-forum.de/)
# based on the Windows GUI exe with same name
 
import urllib, threading, sys

# Configuration (just change here)
boxname = 'speedport.ip'                # or ip (also fritz.box)
password = 'yourpassword'               # your password
protocol = 'https'                      # or http
capfile = 'test.cap'                    # name of capture file

# URL templates
url = protocol + '://' + boxname + '/cgi-bin'       

# Commands
login = 'getpage=../html/de/menus/menu2.html&errorpage=../html/index.html&var:lang=de&var:pagename=home&var:menu=home&=&login:command/password=%s'
start = '/capture_notimeout?start=1&start1=Start'
stop = '/capture_notimeout?stop=1&stop1=Stop'


# Attempt to login
command = urllib.urlopen(url + '/webcm', login % password)
response = command.read()
print 'Login', response

class TraceGetter(threading.Thread):
    def __init__(self, url, filename):
        self.url = url
        self.i = 0
        self.filename = filename
        threading.Thread.__init__(self)
 
    def monitor(self, n1, n2, n3):
        print ["|", "/", "-", "\\"][self.i], "\r",
        self.i += 1
        self.i %= 4
                
    def run(self):
        try:
            urllib.urlretrieve(self.url, self.filename, self.monitor)
            print "Trace stopped"
        except:
            print "Could not open %s" % self.url


thread = TraceGetter(url + start, capfile)
thread.start()
print "Trace started, stop with <ENTER>"
raw_input()
print "Stopping trace"
urllib.urlopen(url + stop)
print "Capture done"
