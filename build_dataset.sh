###########################################################################################################
# This shell script is used to build dataset for the training of our own data using Karpathy's Neuraltalk2#
# Been figuring out how to use MSCOCO, however to no avail. Thus i wanted to create my own datasets       #
# The format of the dataset is simple                                                                     #
# [{ "file_path": "path/img.jpg", "captions": ["a caption", "a similar caption" ...] }, ...]              #
# After finishing the Graphic User Interface (GUI) Process, we then move on to this script.               #
###########################################################################################################

# Copy the kfwtime_final.json file to start the process of creating the new json file

cp ./kfwtime_final.json ./dataset_building/
cd dataset_building/

# Start saving it into a json file that we can use for karpathy
# This will be done mainly in Python

