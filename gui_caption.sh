file="./index_v2.html"

if [ -f "$file" ];
then
    mv ./index.html ./index.html.backup
    mv ./index_v2.html index.html
    mv ./loadvid.js ./loadvid.js.backup
fi


shopt -s nullglob
for file in *.mp4; do 
    video="$file"
done 

filename="${video%.*}"

cat << EOF > loadvid.js
fetchJSONFile('kfwtime_final.json', function (data) {
    // Pass it to global variable
    kfwtimes_final = data;
});

video_player.src="./$video"
vid_subs.src="./$filename.vtt"
video_player.width=640
video_player.height=360
EOF
