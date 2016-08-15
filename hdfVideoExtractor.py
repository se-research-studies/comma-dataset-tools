#!/usr/bin/env python2
# comma.ai Data extractor.
# Copyright (C) 2016 Christian Berger
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
import os
import string
from PIL import Image
from pylab import *
from random import choice

if len(sys.argv) != 2:
    print "\033[1;31;40mError: Missing Parameters, minimum number of parameter is 2 \033[0;37;40m"
    print "Usage: "
    print "       $ hdfVideoExtractor.py input.h5"
    print ""
    sys.exit(234)

f = h5py.File(sys.argv[1], "r")
f.keys()

data = f.get('X')
imgArr = np.zeros((160, 320, 3), 'uint8')

folder = ''.join(choice(string.ascii_letters + string.ascii_uppercase + string.digits) for _ in range(30))
os.popen("mkdir " + folder)

for i, img in enumerate(data):
    red = img[0, :, :]
    green = img[1, :, :]
    blue = img[2, :, :]
    imgArr[:, :, 0] = red
    imgArr[:, :, 1] = green
    imgArr[:, :, 2] = blue
    i3 = im = Image.frombuffer("RGB", (320, 160), imgArr, "raw", "RGB", 0, 1)
    filename = folder + "/" + sys.argv[1].split('.')[0] + "-" + str(i).zfill(9) + ".png"
    i3.save(filename)
    if i == 1000:
        break

call_str = "ffmpeg -f image2 -pattern_type glob -i '" + folder + "/" + sys.argv[1].split('.')[
    0] + "-" + "*.png' -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -qp 0 " + sys.argv[1].split('.')[0] + ".h264"

os.popen(call_str)
#os.popen("rm -rf " + folder)

# Make movie: ffmpeg -f image2 -pattern_type glob -i '*.png' -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -qp 0 cam0.h264
