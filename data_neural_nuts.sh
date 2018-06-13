#!/bin/bash

#preprocess captions saved from im2txt into purely 1 caption per line
# sed -i '/Captions/d' vis.json
# sed -i '/1)/d' vis.json #delete caption 1 as there are 3 per image
# sed -i '/2)/d' vis.json #delete caption 2 as there are 3 per image
# sed -i.bak 's/ (p=.*$//g' vis.json
# sed -i 's/  0) //g' vis.json
# sed -i 's/  1) //g' vis.json
# sed -i 's/  2) //g' vis.json


#write information generated into new vis.json file
echo "[">>vis_neural_nuts.json
imageNum=0
while IFS='' read -r line || [[ -n "$line" ]]; do
	echo "{" >>vis_neural_nuts.json
	echo \"caption\">>vis_neural_nuts.json
	echo ":">>vis_neural_nuts.json
    echo \"$line\">>vis_neural_nuts.json
	echo "," >>vis_neural_nuts.json
	echo \"image_id\">>vis_neural_nuts.json
	echo ":" >>vis_neural_nuts.json
	imageNum=$((imageNum+1))
	echo $imageNum >>vis_neural_nuts.json
	echo "},">>vis_neural_nuts.json
	
done < "$1"
sed -i '$ s/.$//' vis_neural_nuts.json
echo "]">>vis_neural_nuts.json
