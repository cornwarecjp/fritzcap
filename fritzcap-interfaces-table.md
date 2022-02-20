# Observed interfaces on various Fritz!Box models and configurations

## Introduction

The below table has keys, descriptions and Fritz!Box configurations I've observed them on.

This makes it easier to estimate what interface you want to specify with `--cap_interface`.

The table has been assembled by observing various `--show_interfaces` outputs.

Some routers (notably at the one I got from [GH 6490](https://github.com/jpluimers/fritzcap/issues/30#issue-425614620) show the interfaces starting with `1:-` twice with `--show_interfaces`; same for `3001                = Minor = 3001 [':docsis_mng']` . Not why that is yet.

Newer firmwares gain more and more interfaces, but usually just `2-1` and `1-lan` are the first ones to try for capturing VoIP calls.

## Summary

Key                   | English                                        | Deutsch                                        | 7360 124 | 7490 124 | 7490 171 | 7490 178 | 7390 65  | GitHub 0 | GitHub 1 | GH 6490  | Freifunk |
--------------------- | ---------------------------------------------- | ---------------------------------------------- |:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
`1-:acc0`             | :acc0                                          | :acc0                                          |          |          |          |          |          |          |          |     X    |          |
`1-:acc0.4`           | :acc0.4                                        | :acc0.4                                        |          |          |          |          |          |          |          |     X    |          |
`1-:l2sd0`            | :l2sd0                                         | :l2sd0                                         |          |          |          |          |          |          |          |     X    |          |
`1-:l2sd0.2`          | :l2sd0.2                                       | :l2sd0.0                                       |          |          |          |          |          |          |          |     X    |          |
`1-:l2sd0.3`          | :l2sd0.3                                       | :l2sd0.3                                       |          |          |          |          |          |          |          |     X    |          |
`1-:l2sm0`            | :l2sm0                                         | :l2sm0                                         |          |          |          |          |          |          |          |     X    |          |
`1-:lan0`             | :lan0                                          | :lan0                                          |          |          |          |          |          |          |          |     X    |          |
`1-acc0`              | acc0                                           | acc0                                           |          |          |          |          |          |          |          |     X    |          |
`1-acc0.4`            | acc0.4                                         | acc0.4                                         |          |          |          |          |          |          |          |     X    |          |
`1-adsl`              | adsl                                           | adsl                                           |          |          |          |          |          |          |     X    |     X    |          |
`1-ath0`              | ath0                                           | ath0                                           |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |
`1-ath1`              | ath1                                           | ath1                                           |          |     X    |     X    |     X    |     X    |          |     X    |          |     X    |
`1-bat0`              | bat0                                           | bat0                                           |          |          |          |          |          |          |     X    |          |     X    |
`1-dsl`               | dsl                                            | dsl                                            |          |          |          |          |          |          |     X    |          |          |
`1-eth0`              | eth0                                           | eth0                                           |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |
`1-eth1`              | eth1                                           | eth1                                           |     X    |     X    |     X    |     X    |          |     X    |     X    |     X    |          |
`1-eth2`              | eth2                                           | eth2                                           |     X    |     X    |     X    |     X    |          |     X    |     X    |     X    |          |
`1-eth3`              | eth3                                           | eth3                                           |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |
`1-eth_udma0`         | eth_udma0                                      | eth_udma0                                      |          |          |          |          |          |          |          |     X    |          |
`1-eth_udma1`         | eth_udma1                                      | eth_udma1                                      |          |          |          |          |          |          |          |     X    |          |
`1-guest`             | guest                                          | guest                                          |     X    |     X    |     X    |     X    |     X    |          |     X    |     X    |     X    |
`1-guest4`            | guest4                                         | guest4                                         |          |          |     X    |     X    |     X    |          |          |     X    |          |
`1-guest5`            | guest5                                         | guest5                                         |          |          |     X    |     X    |     X    |          |          |     X    |          |
`1-guest_ct1`         | guest_ct1                                      | guest_ct1                                      |     X    |          |          |          |          |          |          |          |     X    |
`1-guest_st1`         | guest_st1                                      | guest_st1                                      |          |     X    |          |          |          |          |          |          |          |
`1-guest_st2`         | guest_st2                                      | guest_st2                                      |          |          |          |          |          |          |          |     X    |          |
`1-guest_st3`         | guest_st3                                      | guest_st3                                      |          |          |          |          |          |          |          |     X    |          |
`1-hotspot`           | hotspot                                        | hotspot                                        |          |          |          |          |          |     X    |          |          |          |
`1-ifb0`              | ifb0                                           | ifb0                                           |          |          |     X    |          |          |          |          |          |          |
`1-ifb1`              | ifb1                                           | ifb1                                           |          |          |     X    |          |          |          |          |          |          |
`1-ing0`              | ing0                                           | ing0                                           |          |          |     X    |          |          |          |          |     X    |          |
`1-lan`               | lan                                            | lan                                            |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |          |
`1-lo`                | lo                                             | lo                                             |          |          |          |          |          |          |     X    |          |     X    |
`1-ppptty`            | ppptty                                         | ppptty                                         |          |          |     X    |          |          |          |          |          |          |
`1-ptm_vr9`           | ptm_vr9                                        | ptm_vr9                                        |     X    |     X    |     X    |     X    |          |          |     X    |          |          |
`1-sit0`              | sit0                                           | sit0                                           |          |          |          |          |          |          |     X    |          |     X    |
`1-tunl0`             | tunl0                                          | tunl0                                          |     X    |     X    |     X    |     X    |          |     X    |     X    |          |          |
`1-vlan_master0`      | vlan_master0                                   | vlan_master0                                   |          |          |          |          |          |          |          |     X    |          |
`1-wan`               | wan                                            | wan                                            |          |          |          |          |     X    |          |          |          |          |
`1-wasp`              | wasp                                           | wasp                                           |          |     X    |     X    |     X    |          |          |     X    |          |     X    |
`1-wdsup1`            | wdsup1                                         | wdsup1                                         |          |          |          |          |          |          |     X    |          |          |
`1-wifi0`             | wifi0                                          | wifi0                                          |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |     X    |
`1-wifi1`             | wifi1                                          | wifi1                                          |          |     X    |     X    |     X    |     X    |          |     X    |     X    |     X    |
`1-wlan`              | wlan                                           | wlan                                           |          |     X    |     X    |     X    |          |          |     X    |          |          |
`1-wlan_guest`        | wlan_guest                                     | wlan_guest                                     |          |          |     X    |     X    |          |          |          |          |          |
`1-wlan_hotspot`      | wlan_hotspot                                   | wlan_hotspot                                   |          |          |     X    |          |          |          |          |          |          |
`1-wlan_wan`          | wlan_wan                                       | wlan_wan                                       |          |          |     X    |          |          |          |          |          |          |
`2-1`                 | 1. Internet connection                         | 1. Internetverbindung                          |     X    |     X    |     X    |     X    |     X    |     X    |          |     X    |          |
`2-2`                 | 2. Internet connection                         | 2. Internetverbindung                          |          |          |          |          |          |          |          |     X    |          |
`2-3`                 | 3. Internet connection                         | 3. Internetverbindung                          |          |          |          |          |          |          |          |     X    |          |
`3-0`                 | Routing interface                              | Routing-Schnittstelle                          |          |     X    |     X    |     X    |     X    |     X    |          |     X    |          |
`3-17`                | Interface 0 ('internet')                       | Schnittstelle 0 ('internet')                   |          |     X    |     X    |     X    |     X    |     X    |          |     X    |          |
`3-18`                | Interface 1 ('iptv')                           | Schnittstelle 1 ('iptv')                       |          |     X    |          |     X    |     X    |          |          |     X    |          |
`3001`                | Minor = 3001 [':docsis_mng']                   | Minor = 3001 [':docsis_mng']                   |          |          |          |          |          |          |          |     X    |          |
`4-128`               | WLAN Management Traffic - Interface 0          | WLAN Management Traffic - Schnittstelle 0      |     X    |     X    |     X    |     X    |     X    |          |          |     X    |          |
`4-129`               | HW (2.4 GHz, wifi0) - Interface 0              | HW (2.4 GHz, wifi0) - Schnittstelle 0          |     X    |     X    |     X    |     X    |     X    |          |          |     X    |          |
`4-130`               | HW2 (2.4 GHz, wifi1) - Interface 0             | HW2 (2.4 GHz, wifi1) - Schnittstelle 0         |          |          |          |          |     X    |     X    |          |          |          |
`4-131`               | AP (2.4 GHz, ath0) - Interface 0               | AP (2.4 GHz, ath0) - Schnittstelle 0           |     X    |     X    |     X    |     X    |          |     X    |          |     X    |          |
`4-132`               | AP (2.4 GHz, ath0) - Interface 1               | AP (2.4 GHz, ath0) - Schnittstelle 1           |     X    |     X    |     X    |     X    |          |     X    |          |     X    |          |
`4-137`               | AP2 (2.4 + 5 GHz, ath1) - Interface 0          | AP2 (2.4 + 5 GHz, ath1) - Schnittstelle 0      |          |     X    |     X    |     X    |          |     X    |          |          |          |
`4-138`               | AP2 (2.4 + 5 GHz, ath1) - Interface 1          | AP2 (2.4 + 5 GHz, ath1) - Schnittstelle 1      |          |     X    |     X    |     X    |          |     X    |          |     X    |          |
`4-141`               | Guest (2.4 GHz, guest4) - Interface 0          | Guest (2.4 GHz, guest4) - Schnittstelle 0      |          |          |     X    |     X    |          |     X    |          |     X    |          |
`4-142`               | Guest (2.4 GHz, guest4) - Interface 1          | Guest (2.4 GHz, guest4) - Schnittstelle 1      |          |          |     X    |     X    |          |     X    |          |     X    |          |
`4-143`               | Guest2 (2.4 + 5 GHz, guest5) - Interface 0     | Guest2 (2.4 + 5 GHz, guest5) - Schnittstelle 0 |          |          |     X    |     X    |          |     X    |          |          |          |
`4-144`               | Guest2 (2.4 + 5 GHz, guest5) - Interface 1     | Guest2 (2.4 + 5 GHz, guest5) - Schnittstelle 1 |          |          |     X    |     X    |          |     X    |          |     X    |          |
`5-201`               | usb1                                           | usb1                                           |          |          |     X    |          |          |          |          |          |          |
`5-202`               | usb2                                           | usb2                                           |          |          |     X    |          |          |          |          |          |          |
`5-161`               | usb1                                           | usb1                                           |     X    |     X    |     X    |     X    |          |     X    |          |     X    |          |
`5-162`               | usb2                                           | usb2                                           |     X    |     X    |     X    |     X    |          |     X    |          |     X    |          |
`5-163`               | usb3                                           | usb3                                           |          |          |          |          |          |          |          |     X    |          |

## Observed devices

Key      | Description
-------- | -----------
7360 124 | Fritz!Box 7360 manually setup: switch on LAN also doing VoIP
7490 124 | Fritz!Box 7490 manually setup: router on fiber network
7490 171 | Fritz!Box 7490 manually setup: router on fiber network also doing VoIP
7490 178 | Fritz!Box 7490 xs4all default configuration: router on fiber network also doing VoIP
GitHub 0 | <https://github.com/rogerGunis/captureAvmFritzboxStream/blob/master/capture.sh>
GitHub 1 | <https://github.com/bittorf/kalua/blob/master/TODO.txt>
GH 6490  | <https://github.com/jpluimers/fritzcap/issues/30#issue-425614620> (Fritz!Box 6490 Cable running FRITZ!OS: 07.02)
Freifunk | <https://forum.freifunk.net/t/anforderung-fuer-mesh-ap-hinter-offloader/14736/27#post_27>

## Notes/explanation on some of these interfaces I've found or deducted. `???` or empty means I still need more information

There is more at <https://boxmatrix.info/wiki/Network-Interfaces> and <https://boxmatrix.info/wiki/Network-Bridges>

Key                   | Explanation                                    | Notes
--------------------- | ---------------------------------------------- | ----
`1-:acc0`             | ???                                            | [acc0](https://boxmatrix.info/wiki/Property:acc0), [acc0](https://www.ip-phone-forum.de/threads/fritz-box-6490-snmp-zugriff-auf-192-168-100-1-nach-update-auf-06-83.294668/page-2) and [acc0](https://www.ip-phone-forum.de/threads/fritz-box-6490-snmp-zugriff-auf-192-168-100-1-nach-update-auf-06-83.294668/)
`1-:acc0.4`           | ???                                            | [acc0.4](https://boxmatrix.info/wiki/Property:acc0.4)
`1-:l2sd0`            | ???                                            | [l2sd0](https://boxmatrix.info/wiki/Property:l2sd0)
`1-:l2sd0.2`          | ???                                            | [l2sd0.2](https://boxmatrix.info/wiki/Property:l2sd0.2)
`1-:l2sd0.3`          | ???                                            | [l2sd0.3](https://boxmatrix.info/wiki/Property:l2sd0.3)
`1-:l2sm0`            | ???                                            | [l2sm0](https://boxmatrix.info/wiki/Property:l2sm0)
`1-:lan0`             | ???                                            | [lan0](https://boxmatrix.info/wiki/Property:lan0)
`1-acc0`              | ???                                            | [acc0](https://boxmatrix.info/wiki/Property:acc0), [acc0](https://www.ip-phone-forum.de/threads/fritz-box-6490-snmp-zugriff-auf-192-168-100-1-nach-update-auf-06-83.294668/page-2) and [acc0](https://www.ip-phone-forum.de/threads/fritz-box-6490-snmp-zugriff-auf-192-168-100-1-nach-update-auf-06-83.294668/)
`1-acc0.4`            | ???                                            | [acc0.4](https://boxmatrix.info/wiki/Property:acc0.4)
`1-adsl`              | ??? ADSL                                       | [adsl](https://boxmatrix.info/wiki/Property:adsl)
`1-ath0`              | WLAN0: First physical Atheros WLAN controller  | [ath0](https://boxmatrix.info/wiki/Property:ath0) The interface of the first `Atheros WLAN` chip.
`1-ath1`              | WLAN1: Second physical Atheros WLAN controller | [ath1](https://boxmatrix.info/wiki/Property:ath1) The interface of the second `Atheros WLAN` chip.
`1-bat0`              | ???                                            | [bat0](https://boxmatrix.info/wiki/Property:bat0)
`1-dsl`               | ??? ADSL                                       | [dsl](https://boxmatrix.info/wiki/Property:dsl) The interface of the `PPP` connection to the `ISP`.
`1-eth0`              | LAN1: First physical Ethernet controller       | [eth0](https://boxmatrix.info/wiki/Property:eth0) The physical `LAN1` port or the integrated `Network-Switch`.
`1-eth1`              | LAN2: First physical Ethernet controller       | [eth1](https://boxmatrix.info/wiki/Property:eth1) The physical `LAN2` port.
`1-eth2`              | LAN3: Third physical Ethernet controller       | [eth2](https://boxmatrix.info/wiki/Property:eth2) The physical `LAN3` port.
`1-eth3`              | LAN4: Fourth physical Ethernet controller      | [eth3](https://boxmatrix.info/wiki/Property:eth3) The physical `LAN4` port.
`1-eth_udma0`         | ???                                            | [eth_udma0](https://boxmatrix.info/wiki/Property:eth_udma0)
`1-eth_udma1`         | ???                                            | [eth_udma1](https://boxmatrix.info/wiki/Property:eth_udma1)
`1-guest`             | ??? LAN bridge for guest access                | [guest](https://boxmatrix.info/wiki/Property:guest) The `LAN` bridge for the `Guest-Network`.
`1-guest4`            | ???                                            | [guest4](https://boxmatrix.info/wiki/Property:guest4)
`1-guest5`            | ???                                            | [guest5](https://boxmatrix.info/wiki/Property:guest5)
`1-guest_ct1`         | l2tp client tunnel                             | [guest_ct1](https://boxmatrix.info/wiki/Property:guest_ct1)
`1-guest_st1`         | l2tp LAN2LAN server tunnel                     | [guest_st1](https://boxmatrix.info/wiki/Property:guest_st1)
`1-guest_st2`         | ???                                            | [guest_st2](https://boxmatrix.info/wiki/Property:guest_st2)
`1-guest_st3`         | ???                                            | [guest_st3](https://boxmatrix.info/wiki/Property:guest_st3)
`1-hotspot`           | ???                                            | [hotspot](https://boxmatrix.info/wiki/Property:hotspot)
`1-ifb0`              | ifb0                                           | [ifb0](https://boxmatrix.info/wiki/Property:ifb0)
`1-ifb1`              | ifb1                                           | [ifb1](https://boxmatrix.info/wiki/Property:ifb1)
`1-ing0`              | ???                                            | [ing0](https://boxmatrix.info/wiki/Property:ing0)
`1-lo`                | 127.0.0.1 LOOPBACK                             | [lo](https://boxmatrix.info/wiki/Property:lo) Local Loopback. Network interface for `localhost`.
`1-lan`               | LAN bridge for regular access                  | all LAN traffic; [lan](https://boxmatrix.info/wiki/Property:lan) The main `LAN` bridge receiving the local box `IP`.
`1-ppptty`            | ppptty                                         | [ppptty](https://boxmatrix.info/wiki/Property:ppptty)
`1-ptm_vr9`           | PPPoE connection                               | [ptm_vr9](https://boxmatrix.info/wiki/Property:ptm_vr9) Interface for the `VDSL2 PTM` mode of the `VR9`.
`1-sit0`              | ???                                            | [sit0](https://boxmatrix.info/wiki/Property:sit0)
`1-tunl0`             | ???                                            | [tunl0](https://boxmatrix.info/wiki/Property:tunl0)
`1-vlan_master0`      | ???                                            | [vlan_master0](https://boxmatrix.info/wiki/Property:vlan_master0)
`1-wan`               | wan                                            | [wan](https://boxmatrix.info/wiki/Property:wan) The physical `WAN` port for some 5-port models or a network bridge.
`1-wasp`              | ???                                            | [wasp](https://boxmatrix.info/wiki/Property:wasp)
`1-wdsup1`            | ???                                            | [wdsup1](https://boxmatrix.info/wiki/Property:wdsup1)
`1-wifi0`             | ???                                            | [wifi0](https://boxmatrix.info/wiki/Property:wifi0)
`1-wifi1`             | ???                                            | [wifi1](https://boxmatrix.info/wiki/Property:wifi1)
`1-wlan`              | WLAN bridge for regular access                 | [wlan](https://boxmatrix.info/wiki/Property:wlan) `VLAN` multiplexer through `wasp`. Joins the `lan` bridge.
`1-wlan_guest`        | WLAN bridge for guest access                   | [wlan_guest](https://boxmatrix.info/wiki/Property:wlan_guest) `VLAN` multiplexer through `wasp`. Joins the `guest` bridge.
`1-wlan_hotspot`      | wlan_hotspot                                   | [wlan_hotspot](https://boxmatrix.info/wiki/Property:wlan_hotspot) `VLAN` multiplexer through `wasp`. Joins the `hotspot` bridge.
`1-wlan_wan`          | wlan_wan                                       | [wlan_wan](https://boxmatrix.info/wiki/Property:wlan_wan) `VLAN` multiplexer through `wasp`. Joins the `wan` bridge.
`2-1`                 | 1. Internet connection                         | Only when configured as router; on Fritz!Box 7360 in switch mode it never seems to show traffic
`2-2`                 | ??? 2. Internet connection                     | Is this used in multi-WAN situations?
`2-3`                 | ??? 3. Internet connection                     | Is this used in multi-WAN situations?
`3-0`                 | ??? Routing interface                          |
`3-17`                | ??? Interface 0 ('internet')                   |
`3-18`                | ??? Interface 1 ('iptv')                       |
`3001`                | ??? Minor = 3001 [':docsis_mng']               |
`4-128`               | ??? WLAN Management Traffic - Interface 0      |
`4-129`               | ??? HW (2.4 GHz, wifi0) - Interface 0          |
`4-130`               | ??? AP 2.4 + 5 GHz wifi0                       |
`4-131`               | ??? AP (2.4 GHz, ath0) - Interface 0           |
`4-132`               | ??? AP (2.4 GHz, ath0) - Interface 1           |
`4-137`               | ??? AP2 (2.4 + 5 GHz, ath1) - Interface 0      |
`4-138`               | ??? AP2 (2.4 + 5 GHz, ath1) - Interface 1      |
`4-141`               | ??? Guest (2.4 GHz, guest4) - Interface 0      |
`4-142`               | ??? Guest (2.4 GHz, guest4) - Interface 1      |
`4-143`               | ??? Guest2 (2.4 + 5 GHz, guest5) - Interface 0 |
`4-144`               | ??? Guest2 (2.4 + 5 GHz, guest5) - Interface 1 |
`5-201`               | usb1                                           | [usb1](https://boxmatrix.info/wiki/Property:usb1)
`5-202`               | usb2                                           | [usb2](https://boxmatrix.info/wiki/Property:usb2)
`5-161`               | ???                                            | [usb1](https://boxmatrix.info/wiki/Property:usb1)
`5-162`               | ???                                            | [usb2](https://boxmatrix.info/wiki/Property:usb2)
`5-163`               | ???                                            | [usb3](https://boxmatrix.info/wiki/Property:usb3) (does not exist yet on `boxmatrix.info` at the time of writing
