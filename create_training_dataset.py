import sys 
import json

json_file = sys.argv[1]
training_file = sys.argv[2]

# json file that you want to add the data into the training dataset
with open(json_file) as f:
    json_data = json.load(f)

# training file that will be fed to Andrej's Karpathy Model
try:
    with open(training_file) as f:
        training_data = json.load(f)
except ValueError:
    training_data = ""

# 
if len(training_data) != 0:    
    
    # Current problem is that the for loop only is the length of the kfwtime_final which let's say is 120 but the
    # training_json
    j = 0
    i = 0
    
    for j in range(len(training_data)):
        if training_data[j]['file_path'] == json_data[0]['relpath']:
            break
        j += 1
    
    for i in range(len(json_data)):
        try:
            if training_data[j+i]['file_path'] == json_data[i]['relpath']:
                training_data[j+i]['captions'].append(json_data[i]['caption'])
        except IndexError: 
            training_data.append({"file_path": json_data[i]['relpath'], "captions":[json_data[i]['caption']]})
        i += 1
        
else:
    training_data = {}
    training_data = []
    
    i = 0

    for i in range(len(json_data)):
        training_data.append({"file_path": json_data[i]['relpath'], "captions":[json_data[i]['caption']]})
        i += 1

with open(training_file, 'w') as fp:
    json.dump(training_data, fp)

print("The data is saved")