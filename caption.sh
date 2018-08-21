#!/bin/bash

set -x
set -e

video_fullpath=$(readlink -m "$1")
imgdir_fullpath=$(readlink -m "$2")

video_dir=$(dirname "$1")
video_filename=$(basename "$1")

mkdir -p "$imgdir_fullpath"
if [ "${video_fullpath##*.}" != 'mp4' ]; then
    /cm/shared/apps/ffmpeg/ffmpeg/bin/ffmpeg -hideb_anner -i "$video_fullpath" "$imgdir_fullpath"'/temp.mp4'
    video_fullpath="$imgdir_fullpath"'/temp.mp4'

    # Update final video directory
    video_dir=$(dirname "$video_fullpath")
    video_filename='temp.mp4'
fi

/cm/shared/apps/ffmpeg/ffmpeg/bin/ffmpeg -hide_banner -i "$video_fullpath" -vf select='gte(scene\,0.1),showinfo' -vsync 2 -y -loglevel info -f null null 2> "$imgdir_fullpath"'/log.txt'
python3 ./get-middle.py -i "$imgdir_fullpath"'/log.txt' -v "$video_fullpath" -d "$imgdir_fullpath"'/%05d.png' -f /cm/shared/apps/ffmpeg/ffmpeg/bin/


cd "$imgdir_fullpath" && mogrify -format jpg *.png
rm *.png && cd ../im2txt/

#im2txt captioning
CHECKPOINT_PATH="./pretrained2m/model2.ckpt-1000000" 
VOCAB_FILE="./pretrained2m/word_counts.txt"
IMAGE_FILE=$(ls $imgdir_fullpath | grep .jpg)

# Build the inference binary.
bazel build -c opt //im2txt:run_inference
#disable gpu during classification
export CUDA_VISIBLE_DEVICES=""

bazel build -c opt //im2txt:run_inference

for IMAGE in $IMAGE_FILE
do
bazel-bin/im2txt/run_inference \
  --checkpoint_path=${CHECKPOINT_PATH} \
  --vocab_file=${VOCAB_FILE} \
  --input_files=${imgdir_fullpath}"/"${IMAGE} >> "$imgdir_fullpath/"'/raw_im2txt.json'
done

cd ../image-caption-generator/

for IMAGE in $IMAGE_FILE
do 
python main.py --mode test --image_path ${imgdir_fullpath}"/"${IMAGE} >> "$imgdir_fullpath/"'/raw_neural_nuts.json'
done

cd ../image_captioning/

for IMAGE in $IMAGE_FILE
do
rm ./test/images/*.jpg
cp ${imgdir_fullpath}"/"${IMAGE} ./test/images/
python main.py --phase=test --model_file='./289999/289999.npy' --beam_size=3 >> "$imgdir_fullpath/"'/raw_image_captioning.json'
done

cd ../neuraltalk2/

for IMAGE in $IMAGE_FILE
do 
rm ./test/images/*.jpg
cp ${imgdir_fullpath}"/"${IMAGE} ./test/images/
th eval.lua -model ./model/model_id1-501-1448236541.t7_cpu.t7 -image_folder ./test/images/ -gpuid -1 -num_images 1  >> "$imgdir_fullpath"'/raw_neuraltalk2.json'
done

cd ../

cp ./data_im2txt.sh "$imgdir_fullpath/"
cp ./data_neural_nuts.sh "$imgdir_fullpath/"
cp ./data_image_captioning.sh "$imgdir_fullpath/"
cp ./data_neuraltalk2.sh "$imgdir_fullpath/"
cd "$imgdir_fullpath/"

#preprocess captions saved from im2txt into purely 1 caption per line
sed -i '/Captions/d' raw_im2txt.json
sed -i '/  1)/d' raw_im2txt.json #delete caption 1 as there are 3 per image
sed -i '/  2)/d' raw_im2txt.json #delete caption 2 as there are 3 per image
sed -i.bak 's/ (p=.*$//g' raw_im2txt.json
sed -i 's/  0) //g' raw_im2txt.json
sed -i 's/  1) //g' raw_im2txt.json
sed -i 's/  2) //g' raw_im2txt.json

./data_im2txt.sh raw_im2txt.json
./data_neural_nuts.sh raw_neural_nuts.json 
./data_image_captioning.sh raw_image_captioning.json
./data_neuraltalk2.sh raw_neuraltalk2.json

cd ../

#####cp ./neuraltalk2/vis/vis.json "$imgdir_fullpath"'/'
python3 ./post-predict.py -v "$video_fullpath" -i "$imgdir_fullpath"'/log.txt' -j "$imgdir_fullpath"'/vis_im2txt.json' -d "$imgdir_fullpath"'/%05d.jpg' -o kfwtime_im2txt.json
python3 ./post-predict.py -v "$video_fullpath" -i "$imgdir_fullpath"'/log.txt' -j "$imgdir_fullpath"'/vis_neural_nuts.json' -d "$imgdir_fullpath"'/%05d.jpg' -o kfwtime_neural_nuts.json
python3 ./post-predict.py -v "$video_fullpath" -i "$imgdir_fullpath"'/log.txt' -j "$imgdir_fullpath"'/vis_image_captioning.json' -d "$imgdir_fullpath"'/%05d.jpg' -o kfwtime_image_captioning.json 
python3 ./post-predict.py -v "$video_fullpath" -i "$imgdir_fullpath"'/log.txt' -j "$imgdir_fullpath"'/vis_neuraltalk2.json' -d "$imgdir_fullpath"'/%05d.jpg' -o kfwtime_neuraltalk2.json

eval $(/cm/shared/apps/ffmpeg/ffmpeg/bin/ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width "$video_fullpath")

### Get the user to check which is the most accurate and thereafter create a kfwtime_final.json
### This command will open a Graphic User Interface which the user then 
python3 ./fyp_gui.py 

# Remove the previous loadvid javascript file catered for another user.
rm -f loadvid.js



cat << EOF > loadvid.js
fetchJSONFile('kfwtime_final.json', function (data) {
    // Pass it to global variable
    kfwtimes_final = data;
});

video_player.src="$(python -c "import os.path; print os.path.relpath('$video_dir', '.')")/$video_filename"
vid_subs.src="./test.vtt"
video_player.width=640
video_player.height=360
EOF



