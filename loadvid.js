fetchJSONFile(' kfwtime_final.json', function (data) {
    // Pass it to global variable
    kfwtimes_final = data;
});

video_player.src="./SIA.mp4"
vid_subs.src="./SIA.vtt"
video_player.width=640
video_player.height=360
