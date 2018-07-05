from tkinter import *
from PIL import ImageTk, Image
import json
from pprint import pprint

### Whats next?
# While loop for the changing of i, need to get the length of json (DONE)
# Saving the selection (Done) & Create the new json file to save these selections
# The next button (save command) (Done)
# The previous button ? (Optional) But i think must do LOLOL
# Then javascript just need one :) (Done)
# GRID (DONE)
# Also create one that the user can type themselves if its not accurate (Today)
# Then the new json file, i will re-train the model again (TODAY)


# import the json files into the GUI
im2txt_path = './kfwtime_im2txt.json'
neural_nuts = './kfwtime_neural_nuts.json'
neuraltalk2 = './kfwtime_neuraltalk2.json'
image_captioning = './kfwtime_image_captioning.json'

# Open the json files
with open(im2txt_path) as f:
    data_im2txt = json.load(f)

with open(neural_nuts) as f:
    data_neural_nuts = json.load(f)

with open(neuraltalk2) as f:
    data_neuraltalk2 = json.load(f)

with open(image_captioning) as f:
    data_imagecaptioning = json.load(f)


# Create a dictionary variable to start storing the caption into 1 json file
final_captions = {}
final_captions= []
i = 0
selection = ""
user_caption = ""

# Image Path of the folder
path = data_im2txt[i]['relpath']
length = len(data_im2txt)
print(length)

# Selected Radio Button
def sel():
    global i
    global selection
    
    if user_caption != "":
        deleteEntry()
        
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
    global user_caption

    selection = ""
    label.config(text="")

    user_caption = Entry(root)
    user_caption.grid(row=8, column=2, sticky=W, padx=10)

def deleteEntry():
    user_caption.destroy()

# Next Button is pressed! 
def nextImage():
    global selection
    global i
    global final_captions

    print(i)
    
    if (selection == "" and user_caption == ""):
        label.config(text="Please select or create a caption!")

    # User Selected caption from radio buttons
    elif selection:
        final_captions.append({
            "start_time":data_im2txt[i]['start_time'],
            "relpath":data_im2txt[i]['relpath'],
            "frame_no":data_im2txt[i]['frame_no'],
            "caption":selection
        })

        selection = ""

        nextImageProcess()

    # User's Typed Caption
    else:
        final_captions.append({
            "start_time":data_im2txt[i]['start_time'],
            "relpath":data_im2txt[i]['relpath'],
            "frame_no":data_im2txt[i]['frame_no'],
            "caption":user_caption.get()
        })

        # pprint(final_captions)
        selection = ""
        deleteEntry()

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
            start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01))
        else:
            start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time']))

        R1.configure(text = data_im2txt[i]['caption'])
        R2.configure(text = data_neural_nuts[i]['caption'])
        R3.configure(text = data_neuraltalk2[i]['caption'])
        R4.configure(text = data_imagecaptioning[i]['caption'])
            
        label.configure(text = "")            
    else:
        next_button.destroy()

        save_button = Button(root, text="Save", command=saveJson)
        save_button.grid(row = 7, column = 1, columnspan = 2, padx = 5)
        
# Saving the json file maybe interesting ? :D
def saveJson():
    global final_captions

    with open('kfwtime_final.json', 'w') as fp:
        json.dump(final_captions, fp)
    
    root.destroy()

# The main part of the GUI (Here we can then adjust into grid from pack!)

root = Tk()

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

# Image File
img = Image.open(path)
img = img.resize((350, 197), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)

panel = Label(root, image = img)
panel.grid(row = 0, column= 1, rowspan = 7, padx = 5, pady = 50)

var = IntVar()

title = Label(root, text="Please select the most accurate caption:")
title.grid(row = 0, column = 2, sticky = W, padx = 5, pady = (50, 0))

start_time = Label(root, text="Start Time: " + str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01))
start_time.grid(row = 1, column = 2, sticky = W, padx = 5)

R1 = Radiobutton(root, text=data_im2txt[i]['caption'], variable=var, value=1,
                    command=sel)
R1.grid(row=2, column = 2, sticky = W)

R2 = Radiobutton(root, text=data_neural_nuts[i]['caption'], variable=var, value=2,
                    command=sel)
R2.grid(row=3, column = 2, sticky = W)

R3 = Radiobutton(root, text=data_neuraltalk2[i]['caption'], variable=var, value=3,
                    command=sel)
R3.grid(row=4, column = 2, sticky = W)

R4 = Radiobutton(root, text=data_imagecaptioning[i]['caption'], variable=var, value=4, command=sel)
R4.grid(row=5, column = 2, sticky = W)

R5 = Radiobutton(root, text="Type your own caption", variable = var, value=5, command = createEntry)
R5.grid(row=6, column=2, sticky = W)

label = Label(root)
label.grid(row=8, column= 1, columnspan = 2, sticky = W+E+N+S)

next_button = Button(root, text="Next", command=nextImage)
next_button.grid(row = 9, column = 1, columnspan = 2)



root.mainloop()