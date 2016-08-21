# comma-dataset-tools

comma-dataset-tools are a small collection of python scripts to convert comma.ai hdf5 files to our OpenDaVINCI .rec format

## hdf2protoRec.py
Converts hdf5 to OpenDaVINCI .rec with message defined in comma.proto. 

Usage:

    ./hdf2protoRec.py messages.h5 output.rec cam0.h264

Where cam0.h264 is the name of the video file extracted from camera-*.h5
Video must be an clean h264 stream do not use containers like .mp4 or .mkv, for ffmpeg simply
use .h264 as file extension.


## hdfVideoExtractor
Extracts all Images form camera-*.h5 and creates a h264 stream, using ffmpeg 
Using command similar to:
"ffmpeg -f image2 -pattern_type glob -i '*.png' -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -qp 0 cam0.h264"

Usage:

    ./hdfVideoExtractor.py input.h5"
    
Command will create random named folder with png files and generates "input.h264" file
You should delete the random named directory after process has finished

##  protoPrint
Prints content of *.rec file on terminal

Usage:

    ./protoPrint.py input.rec

##  Building library for OpenDaVINCI
To build the ODVDCommaAI library, you need to have OpenDaVINCI 4 or later. Let's
assume you have installed OpenDaVINCI 4 at /opt/od4, then you can build this
library as follows:

    mkdir build && cd build
    PATH=/opt/od4/bin:$PATH cmake -D CMAKE_INSTALL_PREFIX=/opt/od4 ..
    make
    make install

##  Building library for OpenDaVINCI with CxxTest
To use CxxTest for the test cases, you need to point CMake to cxxtest:

    mkdir build && cd build
    PATH=/opt/od4/bin:$PATH cmake -D CMAKE_INSTALL_PREFIX=/opt/od4 -D CXXTEST_INCLUDE_DIR=<CxxTest directory> ..
    make
    make install

## playing rec file
For playing the rec files you need, to use odsupercomponent, odcockpit, and odplayerh264. In the standard configuration you need to have a recorder.rec and a corresponding cam0.h264 file
Alternatively you can change the configuration file that odsupercomponent is using. The configuration file must be in the same directory you calling odsupercomponent from.
(you can find one in your OpenDaVINCI install directory "bin/configuration")
All components shold be started with same cid (eg. --cid=123)
First start odsupercomponent, then odcockpit, then change to the folder with the recordings and start odplayerh264 with "--freq=10"
Alter double click on livefeed and on SharedImageViewer you should se something similar to this:

<img src="https://cloud.githubusercontent.com/assets/1830710/17625826/ca3ae1ee-60aa-11e6-86e2-a79d32d8ff50.png" alt="Screenshot">
