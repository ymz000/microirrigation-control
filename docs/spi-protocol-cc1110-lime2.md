# SPI Protocol to Lime2 node #

This small document contains the description of the protocol used over SPI to
communicate to the Lime2 node.
Typically the SPI master is a Linux system (Olimex Lime2 in this project), while
the CC1110 is the SPI slave.
In this document we thus refer to 2 nodes:
 - Lime2 Linux system (SPI master)
 - Lime2 node (SPI slave)

## Overview ##

The protocol follows KISS principles: the Lime2 node firmware just takes whatever
is received over SPI and bridges the received commands over radio.
The commands are acknowledged.
Each command is identified by a "transaction ID" byte.
The transaction ID is a character that will be provided in the ACK response to allow the 
SPI master to associate a sent command with its ACK.

All fields of the packet are ASCII encoded. This makes it easier to use command-line 
utilities (on the Lime2 Linux system) to interact with the SPI bus.

<img src="packet_format.png" />

## Commands ##

As visible on the packet format picture, all commands have a fixed length defined to 
be 7 bytes plus 1 "transaction ID" character plus 1 "command parameter" character.
The commands themselves are ASCII strings. The transaction byte and the command parameter
are ASCII-encoded for simplicity.
So far 3 command strings are supported:
 1. 'TURNON_': signals the remote note that a relay must be turned on
 2. 'TURNOFF': signals the remote note that a relay must be turned off
 3. 'STATUS_': reports battery level of remote node to SPI master

So far 2 command parameters are supported:
 1. '1' to indicate the first relay group
 2. '2' to indicate the second relay group

 Note the final underscores used to pad commands to the 7 bytes length.

As soon as the Lime2 node receives an SPI command from the Lime2 Linux system, 
it will try to communicate over radio with the remote node for about 40 times 
before giving up (about 10secs).

## Acknowledge ##

Every command sent from Lime2 Linux system to the Lime2 node will be acknowledged in the 
opposite direction with a string "ACK_" followed by 1 transaction ID byte.
To receive the acknowledge the SPI master must initiate the communication; this is typically
done by using the "STATUS_" command: the Lime2 node will repeat the acknowledge for the last
command that was successful.

## Testing communication ##

To test commands toward the Lime2 node, you must first verify you have a working setup:
1) log into the Linux system attached via SPI to the Lime2 node.
2) verify you have a device named "/dev/spidev2.0"
3) run
```
      cd /opt && git clone https://github.com/f18m/microirrigation-control.git
      /opt/microirrigation-control/software-lime2/bin/lime2node_cli_backend.php --spi-command TURNON
```
   to send a test command.
4) verify that the YELLOW LED on the "Lime2 node" turns on and the RED LED starts blinking
   slowly. In current firmware implementation each blink of the RED LED means a TX attempt.
5) if the remote node acknowledges the transmission, the PHP utility should return almost immediately.

