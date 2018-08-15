import re
import os
import sys
import csv
import json
import codecs
from getopt import getopt

args = sys.argv[1:]
parsed, args = getopt(args, 'i:j:d:o:v:')

video_filename = ''
stderr_filename = ''
json_filename = ''
imgpath = ''
output_filename = ''
for option, value in parsed:
    if option == '-i':
        stderr_filename = value
    elif option == '-o':
        output_filename = value
    elif option == '-d':
        imgpath = value
    elif option == '-j':
        json_filename = value
    elif option == '-v':
        video_filename = value

if not os.path.isfile(stderr_filename) \
    or not os.path.isfile(json_filename) \
    or not output_filename \
    or not imgpath \
    or not video_filename:
    raise Exception(
'''Missing or incorrect parameters detected! Example usage:
python post-predict.py -v <video_filename> -i <stderr_filename> -j <json_filename> -d <imgpath> -o <output_filename>
python post-predict.py -v Suria102.mp4 -i stderr.txt -j vis.json -d imgs/img%d.jpg -o kfwtime.csv
''')

n = 0
result = [(-1, .0)]
with codecs.open(stderr_filename, mode='r', encoding='utf-8') as stderr_file:
    regex = re.compile('\\[Parsed_showinfo_1 @ [\\w]+] n: {0,3}(\\d+) pts: {0,6}\\d+ pts_time:(\\d+\\.\\d+|\\d+) ')
    for line in stderr_file:
        matches = regex.match(line)

        if matches is None:
            continue

        n = n + 1

        groups = matches.groups()
        # Shift 0-based indexing to 1-based
        frame_id = int(groups[0]) + 1
        start_time = float(groups[1])

        result.append((frame_id, start_time, ))

        assert n == frame_id, 'Missing frame! Expected: %d, received: %d' % (n, frame_id, )

n = n + 1 # to account for frame -1 at t=0s

with codecs.open(json_filename, mode='rb', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

    assert n == len(json_data), 'assert %d == %d error, Number of frames in \'%s\' mismatch \'%s\'!' % (n, len(json_data), stderr_filename, json_filename)

    for entry in json_data:
        caption = entry['caption']
        
        image_id = int(entry['image_id'])
        idx = image_id - 1

        relpath = imgpath % image_id
        assert os.path.isfile(relpath), 'Image %s not found!' % relpath

        result[idx] = result[idx] + (relpath, caption)

# sys.exit()

if '.json' == os.path.splitext(output_filename)[1]:
    result__as_dict = []
    for frame_no, start_time, relpath, caption in result:
        result__as_dict.append({
            'frame_no': frame_no,
            'start_time': start_time,
            'relpath': relpath,
            'caption': caption,
            })

    with codecs.open(output_filename, mode='w', encoding='utf-8') as output_file:
        json.dump(result__as_dict, output_file)

else:
    with codecs.open(output_filename, mode='w', encoding='utf-8') as output_file:
        for frame_no, start_time, relpath, caption in result:
            output_file.write('%s\t%s\t%.4f\t%s\t%s\n' % (video_filename, frame_no, start_time, relpath, caption))

##with open(output_filename, 'w', newline='') as csv_file:
##    csv_writer = csv.writer(csv_file, delimiter=';')
##    csv_writer.writerows(result)
