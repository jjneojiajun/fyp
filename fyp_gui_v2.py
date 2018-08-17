from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import askdirectory
import json
import datetime
import os
from pathlib import Path
from pprint import pprint

# Create a dictionary variable to start storing the caption into 1 json file
final_captions = {}
final_captions= []
i = 0
selection = ""
user_caption = ""
dirname = ""
img = ""
length = 0

data_im2txt = []
data_neural_nuts = []
data_neuraltalk2 = []
data_imagecaptioning = []

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
def NewFile():
    print("New File!")

def OpenFile():
    global dirname
    dirname = askdirectory(initialdir="./", title = "Choose a Directory.") 
    print(dirname)
    loadJson()

def loadJson():
    global data_im2txt
    global data_imagecaptioning
    global data_neural_nuts
    global data_neuraltalk2
    global final_captions
    global i
    global img
    global length

    # import the json files into the GUI
    im2txt_path = dirname + '/kfwtime_im2txt.json'
    neural_nuts = dirname + '/kfwtime_neural_nuts.json'
    neuraltalk2 = dirname + '/kfwtime_neuraltalk2.json'
    image_captioning = dirname + '/kfwtime_image_captioning.json'
    kfwtime_final = Path(dirname + "/kfwtime_final.json")

    if kfwtime_final.exists():
        kfwtime_final = dirname + '/kfwtime_final.json'

        with open(kfwtime_final) as f:
            final_captions = json.load(f)
        
        print(len(final_captions))
            
        if len(final_captions) != 0:
            i = len(final_captions) 

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

    # Image File
    img = Image.open(path)
    img = img.resize((350, 197), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    firstEnable()

def firstEnable():
    panel.config(state="normal", image=img)
    title.config(state="normal")
    start_time.config(state="normal", text="Start Time: " + str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01)[0:3])
    R1.config(state="normal", text=data_im2txt[i]['caption'],)
    R2.config(state="normal", text=data_neural_nuts[i]['caption'],)
    R3.config(state="normal", text=data_neuraltalk2[i]['caption'],)
    R4.config(state="normal", text=data_imagecaptioning[i]['caption'],)
    R5.config(state="normal", text="Type your own captions: ",)
    next_button.config(state="normal")
    previous_button.config(state="normal")


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
    global i
    global final_captions

    previous_button.config(state="normal")

    if (selection == "" and user_caption == ""):
        label.config(text="Please select or create a caption!")

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

        selection = ""
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
        nextImageProcess()
    
    pprint(final_captions)

# This is pretty much duplicate code if i re-use it, thus i created a function simply just for that.
def nextImageProcess():
    global i

    if (i < length-1):
        i += 1

        path = data_im2txt[i]['relpath']

        img2 = Image.open(path)
        img2 = img2.resize((350, 197), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img2)

        panel.configure(image=img2)
        panel.image = img2

        if (i < length-1):
            start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01)[0:3])
        else:
            start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time'])[0:3])

        R1.configure(text = data_im2txt[i]['caption'])
        R2.configure(text = data_neural_nuts[i]['caption'])
        R3.configure(text = data_neuraltalk2[i]['caption'])
        R4.configure(text = data_imagecaptioning[i]['caption'])
            
        label.configure(text = "")            
    else:
        next_button.config(state="disabled")
    
def prevImage():
    global i
    global final_captions

    i = i - 1

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
    else:
        start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time']))

    R1.configure(text = data_im2txt[i]['caption'])
    R2.configure(text = data_neural_nuts[i]['caption'])
    R3.configure(text = data_neuraltalk2[i]['caption'])
    R4.configure(text = data_imagecaptioning[i]['caption'])
            
    label.config(text = "Selected Caption: " + " ' " + final_captions[i]['caption'] + " ' ")

# Saving the json file maybe interesting ? :D
def saveJson():
    global final_captions

    # Remove the past json file
    if dirname + '/kfwtime_final.json' is not None:
        os.remove("kfwtime_final.json")
    
    # Create a new json file
    jsonfile = "kfwtime_final.json"

    with open(jsonfile, 'w') as fp:
        json.dump(final_captions, fp)
    
# The main part of the GUI (Here we can then adjust into grid from pack!)

root = Tk()
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_command(label="Save...", command=saveJson)
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
panel.grid(row = 0, column= 1, rowspan = 9, padx = 5, pady = 50)

var = IntVar()

title = Label(root, state=DISABLED, text="Please select the most accurate caption:")
title.grid(row = 0, column = 2, sticky = W, padx = 5, pady = (50, 0))

start_time = Label(root, state=DISABLED)
start_time.grid(row = 1, column = 2, sticky = W, padx = 5)

R1 = Radiobutton(root, state=DISABLED, variable=var, value=1,
                    command=sel)
R1.grid(row=2, column = 2, sticky = W)

R2 = Radiobutton(root, state=DISABLED, variable=var, value=2,
                    command=sel)
R2.grid(row=3, column = 2, sticky = W)

R3 = Radiobutton(root, state=DISABLED, variable=var, value=3,
                    command=sel)
R3.grid(row=4, column = 2, sticky = W)

R4 = Radiobutton(root, state=DISABLED, variable=var, value=4, command=sel)
R4.grid(row=5, column = 2, sticky = W)

R5 = Radiobutton(root, state=DISABLED, variable = var, value=5, command = createEntry)
R5.grid(row=6, column=2, sticky = W)

user_caption = Entry(root, width = 45, state=DISABLED)
user_caption.grid(row=7, column=2, sticky = (N, W), padx = 25, pady = 5)

label = Label(root)
label.grid(row=8, column= 1, columnspan = 2, sticky = W+E+N+S)

next_button = Button(root, text="Next", state=DISABLED, command=nextImage)
next_button.grid(row = 9, column = 1, columnspan = 2, padx = 10)

previous_button = Button(root, text="Previous", state=DISABLED, command=prevImage)
previous_button.grid(row=9, column = 2, columnspan = 2, padx = 40)

root.mainloop()