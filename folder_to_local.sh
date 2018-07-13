# copy the files into a new directory
# Create the folder to copy into my mac

set -x
set -e

newdir_fullpath = $(readlink -m "$1")
imagefder = $(readlink -m "$2")
videofder = $(readlink -m "$3")

mkdir -p "newdir_fullpath"

cp kfwtime_im2txt.json ./newdir_fullpath
cp kfwtime_image_captioning.json ./newdir_fullpath
cp kfwtime_neural_nuts.json ./newdir_fullpath
cp kfwtime_neualtalk2.json ./newdir_fullpath
cp loadvid.js ./newdir_fullpath
cp imagefder ./newdir_fullpath
cp videofder ./newdir_fullpath


