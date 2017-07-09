# Observed interfaces on various Fritz!Box models and configurations

The below table has keys, descriptions and Fritz!Box configurations I've observed them on.

This makes it easier to estimate what interface you want to specify with `--cap_interface`.

The table has been assembled by observing various `--show_interfaces` outputs.

Key                 | English                                        | Deutsch                                        | 7360 124 | 7490 124 | 7490 171 | 7490 178
------------------- | ---------------------------------------------- | ---------------------------------------------- |:--------:|:--------:|:--------:|:--------:
1-ath0              | ath0                                           | ath0                                           |     X    |     X    |     X    |     X    |
1-ath1              | ath1                                           | ath1                                           |          |     X    |     X    |     X    |
1-eth0              | eth0                                           | eth0                                           |     X    |     X    |     X    |     X    |
1-eth1              | eth1                                           | eth1                                           |     X    |     X    |     X    |     X    |
1-eth2              | eth2                                           | eth2                                           |     X    |     X    |     X    |     X    |
1-eth3              | eth3                                           | eth3                                           |     X    |     X    |     X    |     X    |
1-guest             | guest                                          | guest                                          |     X    |     X    |     X    |     X    |
1-guest4            | guest4                                         | guest4                                         |          |          |     X    |     X    |
1-guest5            | guest5                                         | guest5                                         |          |          |     X    |     X    |
1-guest_ct1         | guest_ct1                                      | guest_ct1                                      |     X    |          |          |          |
1-guest_st1         | guest_st1                                      | guest_st1                                      |          |     X    |          |          |
1-lan               | lan                                            | lan                                            |     X    |     X    |     X    |     X    |
1-ptm_vr9           | ptm_vr9                                        | ptm_vr9                                        |     X    |     X    |     X    |     X    |
1-tunl0             | tunl0                                          | tunl0                                          |     X    |     X    |     X    |     X    |
1-wasp              | wasp                                           | wasp                                           |          |     X    |     X    |     X    |
1-wifi0             | wifi0                                          | wifi0                                          |     X    |     X    |     X    |     X    |
1-wifi1             | wifi1                                          | wifi1                                          |          |     X    |     X    |     X    |
1-wlan              | wlan                                           | wlan                                           |          |     X    |     X    |     X    |
1-wlan_guest        | wlan_guest                                     | wlan_guest                                     |          |          |     X    |     X    |
2-1                 | 1. Internet connection                         | 1. Internetverbindung                          |     X    |     X    |     X    |     X    |
3-0                 | Routing interface                              | Routing-Schnittstelle                          |          |     X    |     X    |     X    |
3-17                | Interface 0 ('internet')                       | Schnittstelle 0 ('internet')                   |          |     X    |     X    |     X    |
3-18                | Interface 1 ('iptv')                           | Schnittstelle 1 ('iptv')                       |          |     X    |          |     X    |
4-128               | WLAN Management Traffic - Interface 0          | WLAN Management Traffic - Schnittstelle 0      |     X    |     X    |     X    |     X    |
4-129               | HW (2.4 GHz, wifi0) - Interface 0              | HW (2.4 GHz, wifi0) - Schnittstelle 0          |     X    |     X    |     X    |     X    |
4-131               | AP (2.4 GHz, ath0) - Interface 0               | AP (2.4 GHz, ath0) - Schnittstelle 0           |     X    |     X    |     X    |     X    |
4-132               | AP (2.4 GHz, ath0) - Interface 1               | AP (2.4 GHz, ath0) - Schnittstelle 1           |     X    |     X    |     X    |     X    |
4-137               | AP2 (2.4 + 5 GHz, ath1) - Interface 0          | AP2 (2.4 + 5 GHz, ath1) - Schnittstelle 0      |          |     X    |     X    |     X    |
4-138               | AP2 (2.4 + 5 GHz, ath1) - Interface 1          | AP2 (2.4 + 5 GHz, ath1) - Schnittstelle 1      |          |     X    |     X    |     X    |
4-141               | Guest (2.4 GHz, guest4) - Interface 0          | Guest (2.4 GHz, guest4) - Schnittstelle 0      |          |          |     X    |     X    |
4-142               | Guest (2.4 GHz, guest4) - Interface 1          | Guest (2.4 GHz, guest4) - Schnittstelle 1      |          |          |     X    |     X    |
4-143               | Guest2 (2.4 + 5 GHz, guest5) - Interface 0     | Guest2 (2.4 + 5 GHz, guest5) - Schnittstelle 0 |          |          |     X    |     X    |
4-144               | Guest2 (2.4 + 5 GHz, guest5) - Interface 1     | Guest2 (2.4 + 5 GHz, guest5) - Schnittstelle 1 |          |          |     X    |     X    |
5-161               | usb1                                           | usb1                                           |     X    |     X    |     X    |     X    |
5-162               | usb2                                           | usb2                                           |     X    |     X    |     X    |     X    |

# Observed devices

Key      | Description
-------- | -----------
7360 124 | Fritz!Box 7360 manually setup: switch on LAN als doing VoIP
7490 124 | Fritz!Box 7490 manually setup: router on fiber network
7490 171 | Fritz!Box 7490 manually setup: router on fiber network also doing VoIP
7490 178 | Fritz!Box 7490 xs4all default configuration: router on fiber network also doing VoIP

# Notes/explanation on some of these interfaces I've found or deducted. `???` or empty means I still need more information.

Key                 | Explanation                                    | Notes
------------------- | ---------------------------------------------- | ----
1-ath0              | WLAN0: First physical Atheros WLAN controller
1-ath1              | WLAN1: Second physical Atheros WLAN controller
1-eth0              | LAN1: First physical Ethernet controller
1-eth1              | LAN2: First physical Ethernet controller
1-eth2              | LAN3: Third physical Ethernet controller
1-eth3              | LAN4: Fourth physical Ethernet controller
1-guest             | ??? LAN bridge for guest access
1-guest4            | ???
1-guest5            | ???
1-guest_ct1         | l2tp client tunnel
1-guest_st1         | l2tp LAN2LAN server tunnel
1-lan               | LAN bridge for regular access                  |  all LAN traffic
1-ptm_vr9           | PPPoE connection
1-tunl0             | ???
1-wasp              | ???
1-wifi0             | ???
1-wifi1             | ???
1-wlan              | WLAN bridge for regular access
1-wlan_guest        | WLAN bridge for guest access
2-1                 | Only when configured as router                 | on Fritz!Box 7360 in switch mode it never seems to show traffic
3-0                 | ??? Routing interface
3-17                | ??? Interface 0 ('internet')
3-18                | ??? Interface 1 ('iptv')
4-128               | ??? WLAN Management Traffic - Interface 0
4-129               | ??? HW (2.4 GHz, wifi0) - Interface 0
4-131               | ??? AP (2.4 GHz, ath0) - Interface 0
4-132               | ??? AP (2.4 GHz, ath0) - Interface 1
4-137               | ??? AP2 (2.4 + 5 GHz, ath1) - Interface 0
4-138               | ??? AP2 (2.4 + 5 GHz, ath1) - Interface 1
4-141               | ??? Guest (2.4 GHz, guest4) - Interface 0
4-142               | ??? Guest (2.4 GHz, guest4) - Interface 1
4-143               | ??? Guest2 (2.4 + 5 GHz, guest5) - Interface 0 |
4-144               | ??? Guest2 (2.4 + 5 GHz, guest5) - Interface 1 |
5-161               | ??? usb1
5-162               | ??? usb2
