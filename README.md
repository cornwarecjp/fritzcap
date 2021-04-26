fritzcap
========

*Fritz!Box trace helper tool*.

```diff
- This project is on hold as I am trying to recover from metastasized rectum cancer as of fall 2019. 
- It is unclear if I will ever be able to put effort in it again.
```

For historic purposes, I've put the [historical 2011-2013 readme at Google Code](https://code.google.com/archive/p/fritzcap/) - which isn't accurate any more - in a [separate file](GoogleCode-README.md).

# Project objectives

This tool simplifies the initiation and termination of [libpcap](https://github.com/the-tcpdump-group/libpcap) compatible traces taken from a FritzBox or SpeedPort (V)DSL router. It may also be used to record and mix captured RTP audio streams (currently G.711 audio only).

Note:

> **Many countries by law forbid authorised recording of (SIP) phone conversations.**

The software may be used in order to debug problems with the local network installation. It is also intended to provide know how on SIP, VOIP and audio data packet formatting/decoding.

- The tool is a Python port of the FritzCap Windows GUI, initially published at [FritzBox: Tool für Etherreal Trace und Audiodaten-Extraktion](http://www.ip-phone-forum.de/showthread.php?t=129725)

- Questions, bug reports and feature requests regarding the current version should be put in the [issues](issues)

- It is not clear how well the current version works on firmware versions older than 06.30. It might be that 1.9.x versions found on the [Google Code repository](https://code.google.com/archive/p/fritzcap/) still work.

# Prerequisites

You need to have Python >= v. 2.6 installed on your machine. Go to http://www.python.org/download/ to find an appropriate download for your system.

# How to enable/disable call monitoring

To enable/disable the CallMonitor option in your Fritz!Box

- Dial `#96*5*` to enable (response "CallMonitor On")
- Dial `#96*4*` to disable (response "CallMonitor Off")

It seems not possible to ask for the current state (enabled/disabled).

After it is enabled, the TCP port 1012 on your Fritz!Box is available

# Examples

## Show the interfaces of a Fritz!Box in default xs4all configuration:

```
# python fritzcap.py --show_interfaces --box_name 192.168.178.1 --password foobar
```

## Capture on router and switch configured Fritz!Box devices:

```
# python fritzcap.py --capture_files --decode_files --monitor_calls --box_name 192.168.171.1 --username foo --password bar
# python fritzcap.py --capture_files --decode_files --monitor_calls --cap_interface 1-lan --box_name 192.168.124.23 --username foo --password bar
```

## Only monitors calls as implicit `root`:

```
# python fritzcap.py --monitor_calls --box_name 192.168.171.1 --password bar
```

Note this will neither capture, nor decode and logs that it cannot capture.

# Command-line options

## version

```
# python fritzcap.py --version
fritzcap.py 2.3
```

## help

```
# feature/re-add_documentation(+0/-0)* ± python fritzcap.py --help
usage: fritzcap.py [-h] [-v] [-c] [-d [file [file ...]]] [-m] [-p password]
                   [-u username] [-s] [--config_file path_to_file]
                   [--logging_config path_to_file] [--box_name host_or_IP]
                   [--call_service_port port] [--login_not_required]
                   [--protocol protocol] [--cap_folder path_pattern]
                   [--cap_file file_pattern] [--cap_interface cap_interface]
                   [--after_capture_time time_in_seconds]
                   [--decode_workers_count int]

fritzcap - audio files analyse

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

main arguments:
  -c, --capture_files   capture file/s. If the monitor option is not set, only
                        one file will be captured
  -d [file [file ...]], --decode_files [file [file ...]]
                        the list of captured files to decode. All the new
                        captures files will be decode automatically if the
                        --capture switch is set. Read the files from the
                        standard input if the list of files is empty and there
                        is no capture work.
  -m, --monitor_calls   start the call monitor mode. The CALL/RING/DISCONNECT
                        events will be used to start/stop the capture
                        automatically
  -p password, --password password
                        the password to login to the box. If not set and
                        --login_not_required is set to False, then the
                        password will be read from the console
  -u username, --username username
                        the username to login to the box (Default:'root')
  -s, --show_interfaces
                        shows the interfaces as key/description pairs

extended defaults arguments:
  --config_file path_to_file
                        the fritzcap configuration file
                        (Default:'fritzcap.conf')
  --logging_config path_to_file
                        the fritzcap logging configuration file
                        (Default:'logging.conf')
  --box_name host_or_IP
                        the host name or IP address of the FritzBox
                        (Default:'fritz.box')
  --call_service_port port
                        the port number of the FritzBox call monitor telnet
                        service (Default:1012)
  --login_not_required  set this flag, if the login is not needed to connect
                        to the box
  --protocol protocol   the protocol to used to login to the FritzBox
                        (Default: 'http')
  --cap_folder path_pattern
                        the folder where the capture files will be stored
                        (Default:'captures/%d%m%Y%H%M/')
  --cap_file file_pattern
                        the file name where the capture data will be saved
                        (Default:'capture.cap')
  --cap_interface cap_interface
                        the key of the interface to capture data from
                        (Default:'3-17' means value 'internet')
  --after_capture_time time_in_seconds
                        time in seconds how long the capture monitor should
                        still continue capture files after all calls were
                        finished (Default:10)
  --decode_workers_count int
                        the count parallel workers to decode captures files.
                        The minimal value is 1 (Default:2).
```

## configuration parameters

Configuration parameters are obtained in this order of importance (from high to low):

1. command-line
2. configuration file (example in [`fritzcap.conf`](fritzcap.conf))
3. defaults (from the above `help`)

# How to obtain?

Source code available here:

- browse at https://github.com/jpluimers/fritzcap
- `git clone https://github.com/jpluimers/fritzcap.git`
- `git clone git@github.com:jpluimers/fritzcap.git`
- download ZIP from https://github.com/jpluimers/fritzcap/archive/master.zip
