#!/usr/bin/env python2
# Copyright (C) 2016 Julian Scholle
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA



import struct
import sys
import time

import comma_pb2

if len(sys.argv) < 2:
    print "\033[1;31;40mError: Missing Parameters, minimum number of parameter is 1 \033[0;37;40m"
    print "Usage: "
    print "       $ protoPrint.py input.rec "
    print ""
    sys.exit(234)

# Print Container's payload.
def extractAndPrintPayload(identifier, p):
    if identifier == 400:  # TestMessage2
        tm = comma_pb2.HDF()
        tm.ParseFromString(p)
        print "Payload: " + str(tm)

    if identifier == 27:  # TestMessage5
        tm = comma_pb2.H264Frame()
        tm.ParseFromString(p)
        print "Payload: " + str(tm)


# Print Container's content.
def printContainer(c):
    print "Container ID = " + str(c.dataType)
    print "Container sent = " + str(c.sent)
    print "Container received = " + str(c.received)
    extractAndPrintPayload(c.dataType, c.serializedData)


# Main.
containers = []

# Read contents from file.
with open(sys.argv[1], "rb") as f:
    print "Reading File, please wait.."

    buf = ""
    bytesRead = 0
    expectedBytes = 0
    LENGTH_OPENDAVINCI_HEADER = 5
    consumedOpenDaVINCIContainerHeader = False

    byte = f.read(1)
    while byte != "":
        buf = buf + byte
        bytesRead = bytesRead + 1

        if consumedOpenDaVINCIContainerHeader:
            expectedBytes = expectedBytes - 1
            if expectedBytes == 0:
                container = comma_pb2.Container()
                container.ParseFromString(buf)
                #containers = containers + [container]

                ## shorten this up...
                printContainer(container)
                # Start over and read next container.
                consumedOpenDaVINCIContainerHeader = False
                bytesRead = 0
                buf = ""

        if not consumedOpenDaVINCIContainerHeader:
            if bytesRead == LENGTH_OPENDAVINCI_HEADER:
                consumedOpenDaVINCIContainerHeader = True
                byte0 = buf[0]
                byte1 = buf[1]

                # Check for OpenDaVINCI header.
                if ord(byte0) == int('0x0D', 16) and ord(byte1) == int('0xA4', 16):
                    v = struct.unpack('<L', buf[1:5])  # Read uint32_t and convert to little endian.
                    expectedBytes = v[0] >> 8  # The second byte belongs to OpenDaVINCI's Container header.
                    buf = ""  # Reset buffer as we will read now the actual serialized data from Protobuf.
                else:
                    print "Failed to consume OpenDaVINCI container."

        # Read next byte.
        byte = f.read(1)

# Print containers.
#print "Found " + str(len(containers)) + " containers."
#for cont in containers:
#    printContainer(cont)
#    time.sleep(0.01)
