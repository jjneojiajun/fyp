from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter.filedialog import askdirectory
import json
import datetime
import os, glob
from pathlib import Path
from pprint import pprint
import subprocess

# Create a dictionary variable to start storing the caption into 1 json file
final_captions = {}
final_captions= []
i = 0
selection = ""
user_caption = ""
dirname = ""
img = ""
video = ""
length = 0
progress_no = 0
duration = ""

data_im2txt = []
data_neural_nuts = []
data_neuraltalk2 = []
data_imagecaptioning = []


im2txt_count = 0
neural_nuts_count = 0
neuraltalk2_count = 0
imagecaptioning_count = 0
user_type_count = 0

final_count = []

print(dirname)

### Whats next?
# While loop for the changing of i, need to get the length of json (DONE)
# Saving the selection (Done) & Create the new json file to save these selections
# The next button (save command) (Done)
# The previous button ? (Optional) But i think must do LOLOL
# GRID (DONE)
# Also create one that the user can type themselves if its not accurate
# Then the new json file, i will re-train the model again

# Load Data and Save Data.
# The new functionality will need to have loading of images and saving of data 
# This mean that we will need to load all the models JSON Path, save into one JSON file and thereafter
# also load the JSON file if the user has completed his selections / typing halfway. 

# The Algorithm for the above functionality is :
# - Load in a folder containing everything:
#   1) Image Folder containing all the images
#   2) JSON Files [im2txt, neural_nuts, neuraltalk2, image_captioning]
#   3) The JSON file to append! 
# - If the JSON file to append is available, go straight to the previous session that the user has completed until.
# - User then carry on his process 
# - Then we will convert the JSON file into srt file to be a subtitle in the video.

# Selected Radio Button
def OpenFile():
    global dirname
    dirname = askdirectory(initialdir=os.getcwd(), title = "Choose a Directory.") 
    print(dirname)
    kfwtime_final = Path(dirname + "/kfwtime_final.json")
    
    if kfwtime_final.exists():
        load_session = initalpop_out() # 1 or 0
        loadJson(load_session)
    else:
        loadJson(0)

def loadJson(load_session):
    global data_im2txt
    global data_imagecaptioning
    global data_neural_nuts
    global data_neuraltalk2
    global final_captions
    global i
    global img
    global length
    global video
    global duration
    global im2txt_count
    global neural_nuts_count
    global neuraltalk2_count
    global imagecaptioning_count
    global user_type_count

    for file in os.listdir(dirname):
        if file.endswith(".mp4"):
            video = file
    
    result = subprocess.Popen(["ffprobe", video],
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
    )

    for x in result.stdout.readlines():
      if b"Duration" in x:
          duration = (x[12:23])
          break

    # import the json files into the GUI
    im2txt_path = dirname + '/kfwtime_im2txt.json'
    neural_nuts = dirname + '/kfwtime_neural_nuts.json'
    neuraltalk2 = dirname + '/kfwtime_neuraltalk2.json'
    image_captioning = dirname + '/kfwtime_image_captioning.json'
    if load_session == 1:
        kfwtime_final = dirname + '/kfwtime_final.json'
        count_json = dirname + "/count.json"

        with open(kfwtime_final) as f:
            final_captions = json.load(f)
            
        with open(count_json) as f:
            count_data = json.load(f)

        im2txt_count = count_data[0]['im2txt_count']
        neural_nuts_count = count_data[0]['neural_nuts_count']
        neuraltalk2_count = count_data[0]['neuraltalk2_count']
        imagecaptioning_count = count_data[0]['imagecaptioning_count']
        user_type_count = count_data[0]['user_type_count']

        print(len(final_captions))
                
        if len(final_captions) != 0:
            i = len(final_captions)-1

    # Open the json files
    with open(im2txt_path) as f:
        data_im2txt = json.load(f)

    with open(neural_nuts) as f:
        data_neural_nuts = json.load(f)

    with open(neuraltalk2) as f:
        data_neuraltalk2 = json.load(f)

    with open(image_captioning) as f:
        data_imagecaptioning = json.load(f)

    # Image Path of the folder
    path = data_im2txt[i]['relpath']
    length = len(data_im2txt)
    print(length)
    i = 0

    # Image File
    img = Image.open(path)
    img = img.resize((350, 197), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    firstEnable()

def firstEnable():
    global progress_no

    progress_no = i + 1
    total_no = len(data_im2txt)

    if progress_no == total_no:
        video_time = str(data_im2txt[i]['start_time']) + " - END "
    else: 
        video_time = str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01)

    if i == 0:
        user_selection = ""
    else: 
        user_selection = str(final_captions[i]['caption'])

    panel.config(state="normal", image=img)
    title.config(state="normal")
    start_time.config(state="normal", text="Start Time: " + video_time)
    video_name.config(state="normal", text="Video File: " + str(video))
    progress.config(state="normal", text= "Progress: " +  str(progress_no) + " / " + str(total_no))
    R1.config(state="normal", text="im2txt: " + data_im2txt[i]['caption'],)
    R2.config(state="normal", text="neural_nuts: " + data_neural_nuts[i]['caption'],)
    R3.config(state="normal", text="neuraltalk2: " + data_neuraltalk2[i]['caption'],)
    R4.config(state="normal", text="imagecaptioning: " + data_imagecaptioning[i]['caption'],)
    R5.config(state="normal", text="Type your own captions: ",)
    label.config(state="normal", text="Selected Caption: " + " ' " + user_selection + " ' ")
    next_button.config(state="normal")
    previous_button.config(state="disabled")

def sel():
    global i
    global selection

    disableEntry()
        
    if var.get() == 1: 
        selection = data_im2txt[i]['caption']
    elif var.get() == 2:
        selection = data_neural_nuts[i]['caption']
    elif var.get() == 3:
        selection = data_neuraltalk2[i]['caption']
    elif var.get() == 4:
        selection = data_imagecaptioning[i]['caption']
    
    label.config(text = "Selected Caption: " + " ' " + selection + " ' ")

def createEntry():
    global selection

    selection = ""
    label.config(text="")

    user_caption.config(state="normal")

def disableEntry():
    user_caption.config(state="disabled")

# Next Button is pressed! 
def nextImage():
    global selection
    global neural_nuts_count
    global neuraltalk2_count
    global im2txt_count
    global imagecaptioning_count
    global user_type_count

    if (selection == "" or user_caption == ""):
        label.config(text="Please select or create a caption!")
        previous_button.config(state="disabled")


    # User Selected caption from radio buttons
    elif selection:
        if len(final_captions) == i: 
            final_captions.append({
                "start_time":data_im2txt[i]['start_time'],
                "relpath":data_im2txt[i]['relpath'],
                "frame_no":data_im2txt[i]['frame_no'],
                "caption":selection
            })
        elif final_captions[i]['caption'] is not None:
            final_captions[i] = {       
                "start_time":data_im2txt[i]['start_time'],
                "relpath":data_im2txt[i]['relpath'],
                "frame_no":data_im2txt[i]['frame_no'],
                "caption":selection
            }

        if var.get() == 1: 
            im2txt_count = im2txt_count + 1
        elif var.get() == 2:
            neural_nuts_count = neural_nuts_count + 1
        elif var.get() == 3:
            neuraltalk2_count = neuraltalk2_count + 1
        elif var.get() == 4:
            imagecaptioning_count = imagecaptioning_count + 1
        else:
            user_type_count = user_type_count + 1

        selection = ""
        previous_button.config(state="normal")
        nextImageProcess()

    # User's Typed Caption
    else:
        if len(final_captions) == i:
            final_captions.append({
                "start_time":data_im2txt[i]['start_time'],
                "relpath":data_im2txt[i]['relpath'],
                "frame_no":data_im2txt[i]['frame_no'],
                "caption":user_caption.get()
            })
        elif final_captions[i]['caption'] is not None:
            final_captions[i] = {       
                "start_time":data_im2txt[i]['start_time'],
                "relpath":data_im2txt[i]['relpath'],
                "frame_no":data_im2txt[i]['frame_no'],
                "caption":user_caption.get()
            }

        # pprint(final_captions)
        selection = ""
        user_caption.delete(0, 'end')
        previous_button.config(state="normal")
        nextImageProcess()
    
    # pprint(final_captions)

# This is pretty much duplicate code if i re-use it, thus i created a function simply just for that.
def nextImageProcess():
    global i
    global progress_no 
    total_no = len(data_im2txt)

    if (i < length-1):
        
        i += 1
        progress_no += 1

        path = data_im2txt[i]['relpath']

        img2 = Image.open(path)
        img2 = img2.resize((350, 197), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img2)

        panel.configure(image=img2)
        panel.image = img2

        if (i < length-1):
            start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01)[0:3])
            progress.config(text= "Progress: " +  str(progress_no) + " / " + str(total_no))
        else:
            start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time'])[0:3] + " - END")
            progress.config(text= "Progress: " +  str(total_no) + " / " + str(total_no))

        R1.configure(text = "im2txt: " + data_im2txt[i]['caption'])
        R2.configure(text = "neural_nuts: " + data_neural_nuts[i]['caption'])
        R3.configure(text = "neuraltalk2: " + data_neuraltalk2[i]['caption'])
        R4.configure(text = "imagecaptioning: " + data_imagecaptioning[i]['caption'])
            
        label.configure(text = "")            
    else:
        next_button.config(state="disabled")
    
def prevImage():
    global i
    global progress_no 
    total_no = len(data_im2txt)

    i = i - 1
    progress_no = progress_no - 1

    if i == 0:
        previous_button.config(state="disabled")

    path = data_im2txt[i]['relpath']

    img2 = Image.open(path)
    img2 = img2.resize((350, 197), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)

    panel.configure(image=img2)
    panel.image = img2

    if (i < length-1):
        start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01))
        progress.config(text= "Progress: " +  str(progress_no) + " / " + str(total_no))
    else:
        start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time']))
        progress.config(text= "Progress: " +  str(progress_no) + " / " + str(total_no))


    R1.configure(text = "im2txt: " + data_im2txt[i]['caption'])
    R2.configure(text = "neural_nuts: " + data_neural_nuts[i]['caption'])
    R3.configure(text = "neuraltalk2: " + data_neuraltalk2[i]['caption'])
    R4.configure(text = "imagecaptioning: " + data_imagecaptioning[i]['caption'])
            
    label.config(text = "Selected Caption: " + " ' " + final_captions[i]['caption'] + " ' ")

# Saving the json file maybe interesting ? :D
def saveJson():
    jsonfile = dirname + "/kfwtime_final.json"

    # Remove the past json file
    try:
        if jsonfile is not None:
            os.remove(jsonfile)

        with open(jsonfile, 'w') as fp:
            json.dump(final_captions, fp)

    except FileNotFoundError:
        with open(jsonfile, 'w') as fp:
            json.dump(final_captions, fp)

    # For the counts

    final_count.append({
        "im2txt_count": im2txt_count,
        "neural_nuts_count": neural_nuts_count,
        "neuraltalk2_count": neuraltalk2_count,
        "imagecaptioning_count": imagecaptioning_count,
        "user_type_count": user_type_count
    })

    countfile = dirname + "/count.json"
    try:
        if countfile is not None:
            os.remove(countfile)

        with open(countfile, 'w') as fp:
            json.dump(final_count, fp)

    except FileNotFoundError:
        with open(countfile, 'w') as fp:
            json.dump(final_count, fp)

    os.system('./gui_caption.sh')

    messagebox.showinfo("File Saved", "Your JSON File is Saved!")

def saveSRT(): 
    saveJson()

    srt_file = dirname + "/" + video[:-4] + ".srt"

    try:
        if srt_file is not None:
            os.remove(srt_file)
    except FileNotFoundError: 
        print("File Not Found! Proceeding Anyways.")

    srt_version = []

    for i in range(0,len(final_captions)):
        if len(final_captions) != i+1 :
            start_minutes = int(final_captions[i]['start_time']/60)
            start_seconds = int(final_captions[i]['start_time'] - (60 * start_minutes))
            start_milliseconds = int((final_captions[i]['start_time'] - (60 * start_minutes) - start_seconds) * 1000000)
            start_time = datetime.time(0,start_minutes, start_seconds, start_milliseconds)

            end_minutes = int(final_captions[i+1]['start_time']/60)
            end_seconds = int(final_captions[i+1]['start_time'] - (60 * end_minutes))
            end_milliseconds = int((final_captions[i+1]['start_time'] - (60 * end_minutes) - end_seconds) * 1000000)
            end_time = datetime.time(0, end_minutes, end_seconds, end_milliseconds)

            srt_version.append({
                "start_time": start_time.strftime('%H:%M:%S,%f'),
                "end_time": end_time.strftime('%H:%M:%S,%f'),
                "caption": final_captions[i]['caption'],
            })
        else: 
            if len(final_captions) == i+1 and len(final_captions) == len(data_im2txt):
                start_minutes = int(final_captions[i]['start_time']/60)
                start_seconds = int(final_captions[i]['start_time'] - (60 * start_minutes))
                start_milliseconds = int((final_captions[i]['start_time'] - (60 * start_minutes) - start_seconds) * 1000000)
                start_time = datetime.time(0,start_minutes, start_seconds, start_milliseconds)

                end_minutes = int(duration.decode("utf-8")[3:5])
                end_seconds = int(duration.decode("utf-8")[6:8])
                end_milliseconds = int(duration.decode("utf-8")[9:])
                end_time = datetime.time(0, end_minutes, end_seconds, end_milliseconds)

                srt_version.append({
                    "start_time": start_time.strftime('%H:%M:%S,%f'),
                    "end_time": end_time.strftime('%H:%M:%S,%f'),
                    "caption": final_captions[i]['caption'],
                })
                
            else:
                start_minutes = int(final_captions[i]['start_time']/60)
                start_seconds = int(final_captions[i]['start_time'] - (60 * start_minutes))
                start_milliseconds = int((final_captions[i]['start_time'] - (60 * start_minutes) - start_seconds) * 1000000)
                start_time = datetime.time(0,start_minutes, start_seconds, start_milliseconds)

                end_minutes = int(data_im2txt[i+1]['start_time']/60)
                end_seconds = int(data_im2txt[i+1]['start_time'] - (60 * end_minutes))
                end_milliseconds = int((data_im2txt[i+1]['start_time'] - (60 * end_minutes) - end_seconds) * 1000000)
                end_time = datetime.time(0, end_minutes, end_seconds, end_milliseconds)
                
                srt_version.append({
                    "start_time": start_time.strftime('%H:%M:%S,%f'),
                    "end_time": end_time.strftime('%H:%M:%S,%f'),
                    "caption": final_captions[i]['caption'],
                })

        i = i + 1

    for i in range(0, len(srt_version)):
        with open(srt_file, 'a') as the_file:
            the_file.write(str(i + 1) + "\n")
            the_file.write(str(srt_version[i]['start_time'][:-3] + " --> " + str(srt_version[i]['end_time'][:-3]) + "\n"))
            the_file.write(srt_version[i]['caption'] + "\n")
            the_file.write("\n")

    messagebox.showinfo("File Saved", "Your srt File is Saved!")

def saveWebVTT():
    saveJson()

    webvtt_file = dirname + "/" + video[:-4] + ".vtt"

    try:
        if webvtt_file is not None:
            os.remove(webvtt_file)
    except FileNotFoundError: 
        print("File Not Found! Proceeding Anyways.")

    webVTT_version = []

    for i in range(0,len(final_captions)):

        if len(final_captions) != i+1:
            start_minutes = int(final_captions[i]['start_time']/60)
            start_seconds = int(final_captions[i]['start_time'] - (60 * start_minutes))
            start_milliseconds = int((final_captions[i]['start_time'] - (60 * start_minutes) - start_seconds) * 1000000)
            start_time = datetime.time(0,start_minutes, start_seconds, start_milliseconds)

            end_minutes = int(final_captions[i+1]['start_time']/60)
            end_seconds = int(final_captions[i+1]['start_time'] - (60 * end_minutes))
            end_milliseconds = int((final_captions[i+1]['start_time'] - (60 * end_minutes) - end_seconds) * 1000000)
            end_time = datetime.time(0, end_minutes, end_seconds, end_milliseconds)

            webVTT_version.append({
                "start_time": start_time.strftime('%M:%S.%f'),
                "end_time": end_time.strftime('%M:%S.%f'),
                "caption": final_captions[i]['caption'],            
            })
        else: 
            if len(final_captions) == i+1 and len(final_captions) == len(data_im2txt):
                start_minutes = int(final_captions[i]['start_time']/60)
                start_seconds = int(final_captions[i]['start_time'] - (60 * start_minutes))
                start_milliseconds = int((final_captions[i]['start_time'] - (60 * start_minutes) - start_seconds) * 1000000)
                start_time = datetime.time(0,start_minutes, start_seconds, start_milliseconds)

                end_minutes = int(duration.decode("utf-8")[3:5])
                end_seconds = int(duration.decode("utf-8")[6:8])
                end_milliseconds = int(duration.decode("utf-8")[9:])
                end_time = datetime.time(0, end_minutes, end_seconds, end_milliseconds)

                webVTT_version.append({
                    "start_time": start_time.strftime('%H:%M:%S,%f'),
                    "end_time": end_time.strftime('%H:%M:%S,%f'),
                    "caption": final_captions[i]['caption'],
                })
                
            else:
                start_minutes = int(final_captions[i]['start_time']/60)
                start_seconds = int(final_captions[i]['start_time'] - (60 * start_minutes))
                start_milliseconds = int((final_captions[i]['start_time'] - (60 * start_minutes) - start_seconds) * 1000000)
                start_time = datetime.time(0,start_minutes, start_seconds, start_milliseconds)

                end_minutes = int(data_im2txt[i+1]['start_time']/60)
                end_seconds = int(data_im2txt[i+1]['start_time'] - (60 * end_minutes))
                end_milliseconds = int((data_im2txt[i+1]['start_time'] - (60 * end_minutes) - end_seconds) * 1000000)
                end_time = datetime.time(0, end_minutes, end_seconds, end_milliseconds)
                
                webVTT_version.append({
                    "start_time": start_time.strftime('%H:%M:%S,%f'),
                    "end_time": end_time.strftime('%H:%M:%S,%f'),
                    "caption": final_captions[i]['caption'],
                })

        i = i + 1
    
    video_vtt = video[:-4] + ".vtt"

    with open(video_vtt, 'a') as vtt_file:
        vtt_file.write("WEBVTT \n")
        vtt_file.write("\n")

    for i in range(0, len(webVTT_version)):
        with open(video_vtt, 'a') as vtt_file:
            vtt_file.write(str(webVTT_version[i]['start_time'][:-3] + " --> " + str(webVTT_version[i]['end_time'][:-3]) + "\n"))
            vtt_file.write(webVTT_version[i]['caption'] + "\n")
            vtt_file.write("\n")

    loadvid = Path(dirname + "/loadvid.js")
    
    # # To allow for user to add the webvtt file into javascript.
    # # Edited the code to test whether it will add the line or not.
    # with open(loadvid, 'r+') as loadvidjs:
    #     for x in loadvidjs:
    #         if str(x) == "vid_subs.src=" + "'./" + video[:-4] + ".vtt'":
    #             break
    #         else:
    #             loadvidjs.write("vid_subs.src=" + "'./" + video[:-4] + ".vtt'")

    messagebox.showinfo("File Saved", "Your WebVTT File is Saved and implemented into the web!")


def initalpop_out():
    result = messagebox.askyesno("Load File","Would you like to Load from Previous Session?")
    value = 0

    if result == True:
        value = 1
    else:
        value = 0

    return value

# The main part of the GUI (Here we can then adjust into grid from pack!)

root = Tk()
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open...", command=OpenFile) # Load Previous Session
filemenu.add_command(label="Save as JSON...", command=saveJson) # Save a Json Will be Used for SRT and WebVTT 
filemenu.add_command(label="Save as SRT...", command=saveSRT)
filemenu.add_command(label="Save as WebVTT...", command=saveWebVTT)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
        
# Defaulting the window
w = 850 # width for the Tk root
h = 450 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

panel = Label(root, state=DISABLED)
panel.grid(row = 0, column= 1, rowspan = 9, padx = 5)

video_name = Label(root, state=DISABLED)
video_name.grid(row = 8, column = 1, padx=5, pady = 45)

var = IntVar()

title = Label(root, state=DISABLED, text="Please select the most accurate caption:")
title.grid(row = 0, column = 2, sticky = W, padx = 5, pady = (70, 0))

start_time = Label(root, state=DISABLED)
start_time.grid(row = 1, column = 2, sticky = W, padx = 5)

progress = Label(root, state=DISABLED)
progress.grid(row = 2, column = 2, sticky = W, padx = 5)

R1 = Radiobutton(root, state=DISABLED, variable=var, value=1,
                    command=sel)
R1.grid(row=3, column = 2, sticky = W, padx = 5)

R2 = Radiobutton(root, state=DISABLED, variable=var, value=2,
                    command=sel)
R2.grid(row=4, column = 2, sticky = W, padx = 5)

R3 = Radiobutton(root, state=DISABLED, variable=var, value=3,
                    command=sel)
R3.grid(row=5, column = 2, sticky = W, padx = 5)

R4 = Radiobutton(root, state=DISABLED, variable=var, value=4, command=sel)
R4.grid(row=6, column = 2, sticky = W, padx = 5)

R5 = Radiobutton(root, state=DISABLED, variable = var, value=5, command = createEntry)
R5.grid(row=7, column=2, sticky = W, padx = 5)

user_caption = Entry(root, width = 45, state=DISABLED)
user_caption.grid(row=8, column=2, sticky = (N, W), padx = 25, pady = 5)

# Bottom of the Video

label = Label(root)
label.grid(row=10, column= 1, columnspan = 2, sticky = W+E+N+S)

previous_button = Button(root, text="Previous", state=DISABLED, command=prevImage)
previous_button.grid(row=11, column = 1 , padx = 30, pady = 20, sticky = E)

next_button = Button(root, text="Next", state=DISABLED, command=nextImage)
next_button.grid(row = 11, column = 2,pady = 20, sticky = W)

root.title("Image Captioning Selection")
root.mainloop()