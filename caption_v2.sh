#!/bin/bash

set -x
set -e

start=`date +%s`

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

#ffmpeg done
end_ffmpeg=`date +%s`
duration_ffmpeg=$((end_ffmpeg-start))

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

#Done With im2txt
end_im2txt=`date +%s`
duration_im2txt=$((end_im2txt-end_ffmpeg))

cd ../image-caption-generator/

for IMAGE in $IMAGE_FILE
do 
python main.py --mode test --image_path ${imgdir_fullpath}"/"${IMAGE} >> "$imgdir_fullpath/"'/raw_neural_nuts.json'
done

end_neural_nuts=`date +%s`
duration_neural_nuts=$((end_neural_nuts-end_im2txt))

cd ../image_captioning/

for IMAGE in $IMAGE_FILE
do
rm ./test/images/*.jpg
cp ${imgdir_fullpath}"/"${IMAGE} ./test/images/
python main.py --phase=test --model_file='./289999/289999.npy' --beam_size=3 >> "$imgdir_fullpath/"'/raw_image_captioning.json'
done

end_image_captioning=`date +%s`
duration_image_captioning=$((end_image_captioning-end_neural_nuts))

cd ../neuraltalk2/

for IMAGE in $IMAGE_FILE
do 
rm ./test/images/*.jpg
cp ${imgdir_fullpath}"/"${IMAGE} ./test/images/
th eval.lua -model ./model/model_id1-501-1448236541.t7_cpu.t7 -image_folder ./test/images/ -gpuid -1 -num_images 1  >> "$imgdir_fullpath"'/raw_neuraltalk2.json'
done

# end of neuraltalk2
end_neuraltalk2=`date +%s`
duration_neuraltalk2=$((end_neuraltalk2-end_image_captioning))

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

name_of_dir=$(basename $imgdir_fullpath)
#####cp ./neuraltalk2/vis/vis.json "$imgdir_fullpath"'/'
python3 ./post-predict.py -v "$video_fullpath" -i "$imgdir_fullpath"'/log.txt' -j "$imgdir_fullpath"'/vis_im2txt.json' -d "./$name_of_dir"'/%05d.jpg' -o kfwtime_im2txt.json
python3 ./post-predict.py -v "$video_fullpath" -i "$imgdir_fullpath"'/log.txt' -j "$imgdir_fullpath"'/vis_neural_nuts.json' -d "./$name_of_dir"'/%05d.jpg' -o kfwtime_neural_nuts.json
python3 ./post-predict.py -v "$video_fullpath" -i "$imgdir_fullpath"'/log.txt' -j "$imgdir_fullpath"'/vis_image_captioning.json' -d "./$name_of_dir"'/%05d.jpg' -o kfwtime_image_captioning.json 
python3 ./post-predict.py -v "$video_fullpath" -i "$imgdir_fullpath"'/log.txt' -j "$imgdir_fullpath"'/vis_neuraltalk2.json' -d "./$name_of_dir"'/%05d.jpg' -o kfwtime_neuraltalk2.json

eval $(/cm/shared/apps/ffmpeg/ffmpeg/bin/ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width "$video_fullpath")

# End of postprediction
end_post_pred=`date +%s`
duration_post_pred=$((end_post_pred-end_neuraltalk2))

rm -f loadvid.js

cat << EOF > loadvid.js
fetchJSONFile('kfwtime_im2txt.json', function (data) {
    // Pass it to global variable
    kfwtimes_im2txt = data;
});

fetchJSONFile('kfwtime_neural_nuts.json', function(data){
    //Pass it to global variable
    kfwtimes_neural_nuts= data;
});

fetchJSONFile('kfwtime_image_captioning.json', function(data){
    // Pass it to global variable
    kfwtimes_image_captioning = data;
});

fetchJSONFile('kfwtime_neuraltalk2.json', function(data){
    // Pass it to global variable
    kfwtimes_neuraltalk2 = data;
});

video_player.src="$(python -c "import os.path; print os.path.relpath('$video_dir', '.')")/$video_filename"
video_player.width=640
video_player.height=360
EOF

# Move everything into one folder
mkdir image_caption_$name_of_dir
mv ./kfwtime_*.json image_caption_$name_of_dir
mv ./loadvid.js image_caption_$name_of_dir
cp ./index.html image_caption_$name_of_dir
cp ./index_v2.html image_caption_$name_of_dir
mv $video_fullpath image_caption_$name_of_dir
mv $imgdir_fullpath image_caption_$name_of_dir
cp ./fyp_gui_v2.py image_caption_$name_of_dir

# End Run
end=`date +%s`
runtime=$((end-start))

cat << EOL > log.txt
Start Time: $start
End Of FFMPEG: $duration_ffmpeg
End Of im2txt: $duration_im2txt
End Of neural_nuts: $duration_neural_nuts
End Of image_captioning: $duration_image_captioning
End Of neuraltalk2: $duration_neuraltalk2
End Of Prediction: $duration_post_pred
End Of System: $runtime
EOL

mv log.txt image_caption_$name_of_dir
