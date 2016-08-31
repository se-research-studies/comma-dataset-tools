# comma-dataset-tools

comma-dataset-tools are a small collection of Python scripts to convert comma.ai hdf5 files to our OpenDaVINCI .rec format for further experimentation.


## hdf2protoRec.py
Converts hdf5 to OpenDaVINCI .rec with message defined in comma.proto. 

Usage:

    ./hdf2protoRec.py messages.h5 output.rec cam0.h264

Where cam0.h264 is the name of the video file extracted from camera-*.h5 file. The video must be a clean h264 stream and not a container format like .mp4 or .mkv; the file extension .h264 works nicely.


## hdfVideoExtractor
Extracts all images from a camera-*.h5 file and creates an h264 stream; the final ffmpeg call is similar to:

    ffmpeg -f image2 -pattern_type glob -i '*.png' -vcodec libx264 -pix_fmt yuv420p -preset ultrafast -qp 0 cam0.h264

Usage:

    ./hdfVideoExtractor.py input.h5
    
The command will create a randomly named folder to store the extracted PNG files and generates a file called "input.h264". You can  delete the randomly named directory after process has finished.

##  protoPrint
Prints the content a .rec file to stdout.

Usage:

    ./protoPrint.py input.rec

<img src="https://raw.githubusercontent.com/se-research-studies/comma-dataset-tools/master/odcockpit.gif" alt="Screenshot">
