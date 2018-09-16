fetchJSONFile('kfwtime_im2txt.json', function (data) {
    // Pass it to global variable
    kfwtimes_final = data;
});

fetchJSONFile('kfwtime_image_caption.json', function (data) {
    // Pass it to global variable
    kfwtimes_final = data;
});

fetchJSONFile('kfwtime_neural_nuts.json', function (data) {
    // Pass it to global variable
    kfwtimes_final = data;
});

fetchJSONFile('kfwtime_neuraltalk2.json', function (data) {
    // Pass it to global variable
    kfwtimes_final = data;
});


video_player.src="./"
vid_subs.src="./.vtt"
video_player.width=640
video_player.height=360
