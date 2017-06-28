fritzcap
========

*FritzBox trace helper tool*

# Project objectives

This tool simplifies the initiation and termination of libpcap compatible traces taken from a FritzBox or SpeedPort (V)DSL router. It may also be used to record and mix captured RTP audio streams (currently G.711 audio only).

**The tool is a Python port of the FritzCap Windows GUI, initially published here:** http://www.ip-phone-forum.de/showthread.php?t=129725

**2011/03/22: Questions regarding the current version should be discussed here:** http://www.ip-phone-forum.de/showthread.php?t=232682

**2013/03/03: Current FW for 7390 and others breaks the script (content changes). In order to make it run on 7390, FRITZ!OS 05.50, Firmware-Version 84.05.50 a small patch was applied to featured download 1.9.1_r12

Note: It is not permitted by law to use the provided software for unauthorized recordings of SIP phone conversations.**

The software may be used in order to debug problems with the local network installation. It is also intended to provide know how on SIP, VOIP and audio data packet formatting/decoding.

# Prerequisites

You need to have Python >= v. 2.6 installed on your machine. Go to http://www.python.org/download/ to find an appropriate download for your system.

# How to obtain?

Source code available here http://code.google.com/p/fritzcap/source/checkout. Follow the instructions given to check out the latest revision using SVN or other tools or go to http://code.google.com/p/fritzcap/source/browse/#svn/trunk to download manually.

# How to use?

- Edit the configuration section in "fritzcap.py" and adapt it to your environment (e.g. name or ip address of the FritzBox/SpeedPort router, whether or not login is required, a password, etc.).
- Launch "fritzcap.py". Stop the capture with ENTER, whenever you like.
- The captured data is contained in a folder named according to the current date and time under the subfolder "captures". By default G.711 audio is extracted to separate streams.
- If audio mixing is enabled (yes by default), paired streams are mixed and saved to disk as 16 bit linear PCM audio (Windows WAV format). If mixing is not enabled, streams may also be left unchanged and saved to disk as raw G.711 WAV files (set parameters "linearize" and "mix" to 0 then while instantiating a G711Decoder object in "fritzcap.py")

Right now the audio extraction and mix is done not in real time, but after a voice conversation has been finished. This is by design of the capturing process currently.

# Tests so far

All functionalities have been tested using Python 2.6, a SpeedPort W 920 V on a 25 MBit/s VDSL line as well as against FritzBox Fon WLAN. SID authentication has been successfully tested and made run by valuable assistance of the IP-Phone forum user **LunatiCat** (http://www.ip-phone-forum.de).

# Known issues

The audio extraction and mixing is roughly ten times slower than the previous native C++ implementation of ALEACH.EXE (see the genuine FritzCap package). This is primarily caused by the Python script execution. Optimizations welcome.

# Future work

Probably someone wants to add G.721 decoding in the future.

*Last edited: 2013/03/03*
