import os
import re
import sys
import codecs
from getopt import getopt
from subprocess import Popen, PIPE

args = sys.argv[1:]
parsed, args = getopt(args, 'i:v:d:f:')

stderr_filename = ''
video_filename = ''
imgpath = ''
ffmpeg_path = ''
for option, value in parsed:
    if option == '-i':
        stderr_filename = value
    elif option == '-v':
        video_filename = value
    elif option == '-d':
        imgpath = value
    elif option == '-f':
        ffmpeg_path = value

if not os.path.isfile(stderr_filename) or not os.path.isfile(video_filename) or not imgpath:
    raise Exception(
'''Missing or incorrect parameters detected! Example usage:
python get-middle.py -i <stderr_filename> -v <video_filename> -d <imgpath> [-f <ffmpeg_path>]
python get-middle.py -i Suria102/stderr.txt -v Suria102.mp4 -d Suria102/middle-%04d.png -f ~/bin/
''')

expected_frame_id = 0
result = [(-1, .0)]
with open(stderr_filename, 'r', encoding='utf-8') as stderr_file:
    regex = re.compile('\\[Parsed_showinfo_1 @ [\\w]+] n: {0,3}(\\d+) pts: {0,6}\\d+ pts_time:(\\d+\\.\\d+|\\d+) ')
    for line in stderr_file:
        matches = regex.match(line)

        if matches is None:
            continue

        expected_frame_id = expected_frame_id + 1

        groups = matches.groups()
        # Shift 0-based indexing to 1-based
        frame_id = int(groups[0]) + 1
        time = float(groups[1])

        result.append((frame_id, time, ))

        assert expected_frame_id == frame_id, 'Missing frame! Expected: %d, received: %d' % (expected_frame_id, frame_id, )

# ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <video_filename>
command = '\'%s\'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \'%s\'' % (ffmpeg_path, video_filename)
proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
proc_out, _ = proc.communicate()

next_frame_id = 0
video_duration = float(proc_out)

assert len(result) > 0, "No keyframe found!?"

for i in range(1, len(result)):
    t_start = result[i - 1][1]
    t_middle = t_start + (result[i][1] - t_start) / 2.

    next_frame_id = next_frame_id + 1

    # ffmpeg -ss <t_middle> -i <video_filename> -vframes 1 <imgpath>
    ffmpeg_command = '\'%s\'ffmpeg -y -hide_banner -v quiet -ss %.6f -i \'%s\' -vframes 1 \'%s\'' % (ffmpeg_path, t_middle, video_filename, imgpath % next_frame_id)
    
    ffmpeg_proc = Popen(ffmpeg_command, shell=True)
    ffmpeg_proc.communicate()


# The very last frame!
t_start = result[-1][1]
t_middle = t_start + (video_duration - t_start) / 2.

next_frame_id = next_frame_id + 1

ffmpeg_command = '\'%s\'ffmpeg -y -hide_banner -v quiet -ss %.6f -i \'%s\' -vframes 1 \'%s\'' % (ffmpeg_path, t_middle, video_filename, imgpath % next_frame_id)
ffmpeg_proc = Popen(ffmpeg_command, shell=True)
ffmpeg_proc.communicate()
