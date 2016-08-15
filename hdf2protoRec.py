#!/usr/bin/env python2
# comma.ai Data extractor.
# Copyright (C) 2016 Julian Scholle
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
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


import h5py
import math
import struct
import sys
import time

import comma_pb2

if len(sys.argv) < 4:
    print "\033[1;31;40mError: Missing Parameters, minimum number of parameter is 3 \033[0;37;40m"
    print "Usage: "
    print "       $ hdf2protoRec.py input.h5 output.rec cam0.h264"
    print ""
    sys.exit(234)

# for handling 	asynchronous timestamps
class AsyncData:
    def __init__(self, data, stamps):
        self.data = data
        self.stamps = stamps
        self.size = data.shape[0] - 1
        self.idx = 0

    def getDataforTime(self, time, delta):
        data = []
        while (self.idx < self.size and self.stamps[self.idx] - time < delta):
            data.append((self.stamps[self.idx], self.data[self.idx]))
            self.idx += 1
        return data


messages = h5py.File(sys.argv[1], "r")
data_size = len(messages['idx'])
framePointers = AsyncData(messages['UN_D_cam1_ptr'], messages['UN_T_cam1_ptr'])
etr = 0


start = time.time()
with open(sys.argv[2], "w") as f:
    for i in xrange(data_size):
        cont = comma_pb2.Container()
        cont.dataType = 400
        cont.sent.seconds = int(messages['times'][i])
        cont.sent.microseconds = int(((messages['times'][i]) - int(messages['times'][i])) * 1000000)
        cont.received.seconds = int(messages['times'][i])
        cont.received.microseconds = int(((messages['times'][i]) - int(messages['times'][i])) * 1000000)
        hdf = comma_pb2.HDF()
        hdf.blinker = bool(messages['blinker'][i])
        hdf.brake = int(messages['brake'][i])
        hdf.brake_computer = bool(messages['brake_computer'][i])
        hdf.brake_user = int(messages['brake_user'][i])
        hdf.car_accel = float(messages['car_accel'][i])
        hdf.fiber_accel_x = float(messages['fiber_accel'][i][0])
        hdf.fiber_accel_y = float(messages['fiber_accel'][i][1])
        hdf.fiber_accel_z = float(messages['fiber_accel'][i][2])
        hdf.fiber_compass_x = float(messages['fiber_compass_x'][i])
        hdf.fiber_compass_y = float(messages['fiber_compass_y'][i])
        hdf.fiber_compass_z = float(messages['fiber_compass_z'][i])
        hdf.fiber_gyro_x = float(messages['fiber_gyro'][i][0])
        hdf.fiber_gyro_y = float(messages['fiber_gyro'][i][1])
        hdf.fiber_gyro_z = float(messages['fiber_gyro'][i][2])
        hdf.gas = float(messages['gas'][i])
        hdf.gear_choice = float(messages['gear_choice'][i])
        hdf.rpm = float(messages['rpm'][i])
        hdf.rpm_post_torque = float(messages['rpm_post_torque'][i])
        hdf.selfdrive = bool(messages['selfdrive'][i])
        hdf.speed = float(messages['speed'][i])
        hdf.speed_abs = float(messages['speed_abs'][i])
        hdf.speed_fl = float(messages['speed_fl'][i])
        hdf.speed_fr = float(messages['speed_fr'][i])
        hdf.speed_rl = float(messages['speed_rl'][i])
        hdf.speed_rr = float(messages['speed_rr'][i])
        hdf.standstill = bool(messages['standstill'][i])
        hdf.steering_angle = math.radians((messages['steering_angle'][i]))
        hdf.steering_torque = float(messages['steering_torque'][i])
        hdf.velodyne_gps_latitude = float(messages['velodyne_gps'][i][0]) / 60.0
        hdf.velodyne_gps_longitude = float(messages['velodyne_gps'][i][1]) / 60.0
        hdf.velodyne_heading = math.radians((messages['velodyne_heading'][i][0]))
        cont.serializedData = hdf.SerializeToString()
        data = cont.SerializeToString()

        length = len(data)
        f.write(struct.pack("<BB", *bytearray([0x0D, 0xA4])))
        f.write(struct.pack("<BBB", *bytearray([length >> bit & 0xff for bit in (0, 8, 16)])))
        f.write(data)

        frameData = framePointers.getDataforTime(messages['times'][i], 0)

        for frame in frameData:
            cont = comma_pb2.Container()
            cont.dataType = 27
            cont.sent.seconds = int(frame[0])
            cont.sent.microseconds = int(((frame[0]) - int(frame[0])) * 1000000)
            cont.received.seconds = int(frame[0])
            cont.received.microseconds = int(((frame[0]) - int(frame[0])) * 1000000)
            h264 = comma_pb2.H264Frame()
            h264.h264Filename = sys.argv[3]
            h264.frameIdentifier = frame[1]
            h264.frameSize = 0
            h264.associatedSharedImage.name = "cam0"
            h264.associatedSharedImage.size = 320 * 160 * 3
            h264.associatedSharedImage.width = 320
            h264.associatedSharedImage.height = 160
            h264.associatedSharedImage.bytesPerPixel = 3
            cont.serializedData = h264.SerializeToString()
            data = cont.SerializeToString()

            length = len(data)
            f.write(struct.pack("<BB", *bytearray([0x0D, 0xA4])))
            f.write(struct.pack("<BBB", *bytearray([length >> bit & 0xff for bit in (0, 8, 16)])))
            f.write(data)

        if i % 100 == 0:
            elapsed = time.time() - start
            if i > 0:
                etr = (1 - i / float(data_size)) * (elapsed / (i / float(data_size)))
            sys.stdout.write("Download progress: %d%%   %d/%d  estimated: %d min \r" % (int((i / float(data_size)) * 100), i, data_size, (etr / 60)+0.5))
            sys.stdout.flush()

print "\nFinished in %.2f sec!" % (time.time() - start)
