shopt -s nullglob
for file in *.mp4; do 
    video="$file"
done 

filename="${video%.*}"

cat << EOF > loadvid.js
fetchJSONFile('kfwtime_final.json', function (data) {
    // Pass it to global variable
    kfwtimes_im2txt = data;
});

video_player.src="./$video"
vid_subs.src="./$filename.vtt"
video_player.width=640
video_player.height=360
EOF
