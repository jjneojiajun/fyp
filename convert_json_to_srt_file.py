import json
import datetime
import time

with open('kfwtime_final.json') as f:
    kfwtime_data = json.load(f)

srt_version = []

for i in range(0,len(kfwtime_data)):
    if i == len(kfwtime_data)-1:
        start_minutes = int(kfwtime_data[i]['start_time']/60)
        start_seconds = int(kfwtime_data[i]['start_time'] - (60 * start_minutes))
        start_milliseconds = int((kfwtime_data[i]['start_time'] - (60 * start_minutes) - start_seconds) * 1000000)
        start_time = datetime.time(0,start_minutes, start_seconds, start_milliseconds)
        
        # add the ffmpeg duration for the video
    
    else:
        start_minutes = int(kfwtime_data[i]['start_time']/60)
        start_seconds = int(kfwtime_data[i]['start_time'] - (60 * start_minutes))
        start_milliseconds = int((kfwtime_data[i]['start_time'] - (60 * start_minutes) - start_seconds) * 1000000)
        start_time = datetime.time(0,start_minutes, start_seconds, start_milliseconds)

        end_minutes = int(kfwtime_data[i+1]['start_time']/60)
        end_seconds = int(kfwtime_data[i+1]['start_time'] - (60 * end_minutes))
        end_milliseconds = int((kfwtime_data[i+1]['start_time'] - (60 * end_minutes) - end_seconds) * 1000000)
        end_time = datetime.time(0, end_minutes, end_seconds, end_milliseconds)

        duration = kfwtime_data[i+1]['start_time'] - kfwtime_data[i]['start_time']

        srt_version.append({
            "start_time": start_time.strftime('%H:%M:%S,%f'),
            "end_time": end_time.strftime('%H:%M:%S,%f'),
            "caption": kfwtime_data[i]['caption'],
            "duration": duration
        })

    i = i + 1

for i in range(0, len(srt_version)):
    with open('test.srt', 'a') as the_file:
        the_file.write(str(i + 1) + "\n")
        the_file.write(str(srt_version[i]['start_time'][:-3] + " --> " + str(srt_version[i]['end_time'][:-3]) + "\n"))
        the_file.write(srt_version[i]['caption'] + "\n")
        the_file.write("\n")
