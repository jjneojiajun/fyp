from tkinter import *
from PIL import ImageTk, Image
import json
from pprint import pprint

### Whats next?
# While loop for the changing of i, need to get the length of json (DONE)
# Saving the selection (Done) & Create the new json file to save these selections
# The next button (save command) (Done)
# The previous button ? (Optional) But i think must do LOLOL
# Then javascript just need one :) 
# Also create one that the user can type themselves if its not accurate 
# Then the new json file, i will re-train the model again 


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


# Create a variable to start storing the caption into 1 json file
final_captions = {}
final_captions= []
i = 0
selection = ""

# Image Path of the folder
path = data_im2txt[i]['relpath']
length = len(data_im2txt)
print(length)

# Selected Radio Button
def sel():
    global i
    global selection

    if var.get() == 1: 
        selection = data_im2txt[i]['caption']
    elif var.get() == 2:
        selection = data_neural_nuts[i]['caption']
    elif var.get() == 3:
        selection = data_neuraltalk2[i]['caption']
    else:
        selection = data_imagecaptioning[i]['caption']
    
    label.config(text = selection)

def nextImage():
    global selection
    global i
    global final_captions

    final_captions.append({
        "start_time":data_im2txt[i]['start_time'],
        "relpath":data_im2txt[i]['relpath'],
        "frame_no":data_im2txt[i]['frame_no'],
        "caption":selection
    })

    pprint(final_captions)

    i += 1

    path = data_im2txt[i]['relpath']

    img2 = Image.open(path)
    img2 = img2.resize((256, 154), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)

    panel.configure(image=img2)
    panel.image = img2

    start_time.configure(text="Start Time: " + str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01))

    R1.configure(text = data_im2txt[i]['caption'])
    R2.configure(text = data_neural_nuts[i]['caption'])
    R3.configure(text = data_neuraltalk2[i]['caption'])
    R4.configure(text = data_imagecaptioning[i]['caption'])

    label.configure(text = "")

root = Tk()
img = Image.open(path)
img = img.resize((256, 144), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)

panel = Label(root, image = img)
panel.pack(side = "top", expand = "no", pady=10)

var = IntVar()

title = Label(root, text="Please select the most accurate caption:")
title.pack(anchor=W)

start_time = Label(root, text="Start Time: " + str(data_im2txt[i]['start_time']) + " - " + str(data_im2txt[i+1]['start_time']-0.01))
start_time.pack(anchor=W, pady=10)

R1 = Radiobutton(root, text=data_im2txt[i]['caption'], variable=var, value=1,
                  command=sel)
R1.pack()

R2 = Radiobutton(root, text=data_neural_nuts[i]['caption'], variable=var, value=2,
                  command=sel)
R2.pack()

R3 = Radiobutton(root, text=data_neuraltalk2[i]['caption'], variable=var, value=3,
                  command=sel)
R3.pack()

R4 = Radiobutton(root, text=data_imagecaptioning[i]['caption'], variable=var, value=4, command=sel)
R4.pack()

label = Label(root)
label.pack()

next_button = Button(root, text="Next", command=nextImage)
next_button.pack(side=RIGHT)

root.mainloop()