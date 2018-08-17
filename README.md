# Final Year Project (Image Captioning)

As technology improves as the years goes on, the image captioning technology improves along the way as well. We have im2txt from Google, neuraltalk2 by Andrej Karpathy and so much more. What I am trying to do is basically using video, split them into frame by frame and decode it using these technologies. I managed to garner 4 image captioning models and generate a caption from them. 

However, it doesn't make any sense to have 4 captions in the video and thus i decided to create a GUI to allow users from running the script that creates the 4 captions to be able to select which is the most accurate caption! Or we can allow the user to type in their own captions as well. 

Although, the user would have to follow the caption style that is used in most of the NLP Module. I believe that this is the best way to do it thus far. After the user key in the caption, it will be great to retrain the model which is what i will be doing right after. 

An example of the caption is: "a women is smiling behind the city view."

# The overall flow of the project is as follow:

![alt text](https://imgur.com/a/xyIecHF)

There are 2 parts of the process flow. We aim to mainly automate the process unless where we require human input where the Graphic User Interface (GUI) is created for the human input. 

We create a "Production House" which consist of 4 image captioning models where we break down a video using FFMPEG into a series of images that will be fed through the "production house" into 4 json files.

After these 4 json files are generated, we will then move onto the graphic user interface where the user select the most accurate captions or type their own captions to be stored into a final json file which we after convert the json file to a srt file.

### What is a SRT File?
If you are not from a video production company or deal with subtitles before. 

The srt file will allow us to edit the start time and end time as well as the caption as well. However it is not recommended since we have done that after the GUI.

# GUI Example 
Note that this is not the complete one. This is just an example that i did thus far using python tkinter code which is available to read at this repository at fyp_gui. Note that it will be different for different OS.

![alt text](https://i.imgur.com/TIeNlxn.png)

As of 16th August 2018, these are the functionalities:
* Open Directory
* Select Captions
* Save Current Session 
* Load from Previous Session 
* User Type Captions

# Results (Video)
After creating srt file, we will then be able to add the srt file into the video. Tested in VLC ![VLC Website](https://www.videolan.org/vlc/index.html).

The result will look something like this:
![alt text]()

Video tested with Singapore Airlines Safety Video

# Progamming Languages
The main programming language is using bash and python 3.6

# Credits 
Credits got to go to credit due. 

im2txt - Google
Neuraltalk2 - Andrej Karpathy, Stanford
neural_nuts - 
Show and Tell - University Of Toronto

