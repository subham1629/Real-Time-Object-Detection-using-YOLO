import tkinter as tk
import tkinter.filedialog
import cv2
import PIL.Image
import PIL.ImageTk
import time
import os


class App:
    def __init__(self, master, window, window_title, video_source=0):
        # Create a window
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1535x785+0+0")
        self.window.configure(background="lightblue")
        self.video_source = video_source

        self.create_title()
        # self.grid()

    def create_title(self):
        # Create title label for Program
        self.button1 = tk.Button(self.window, text="Open Camera", font=(
            "Arial", 16, "bold"),bg="lightgreen", command=self.open_camera, height=1, width=12)
        self.button1.place(x=560, y=90)

    def open_camera(self):
        # open webcam
        self.win1 = tk.Toplevel()
        self.win1.geometry("652x520+16+160")
        self.app = Demo(self.win1, "Webcam")
  

class Demo:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_capture = tk.Button(window, text="Capture", font=("Arial", 12, "bold"),bg="magenta",width=25, command=self.snapshot)
        self.btn_capture.place(x=35, y=484)

        self.btn_close = tk.Button(window, text="Close Camera", font=("Arial", 12, "bold"),bg="magenta",width=25, command=window.destroy)
        self.btn_close.place(x=350, y=484)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        self.window.quit()
        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("test.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)
    

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def show():
    load = PIL.Image.open("test.jpg")
    render = PIL.ImageTk.PhotoImage(load)
    img = tk.Label(root,image=render)
    img.image = render
    img.place(x=20, y=160)

def browse():
    fname = tk.filedialog.askopenfilename()
    image = PIL.Image.open(fname)
    new_image = image.resize((640,480)) 
    new_image.save('test.jpg')

def run():
    os.system('python yolo.py --image test.jpg --yolo yolo-coco')


def display():
    load = PIL.Image.open("output.jpg")
    render = PIL.ImageTk.PhotoImage(load)
    img = tk.Label(root,image=render)
    img.image = render
    img.place(x=860, y=160)    


# Main manager
root = tk.Tk()

# Background Image
bg = PIL.Image.open("back2.jpg")
bg_img = PIL.ImageTk.PhotoImage(bg)
img = tk.Label(root,image = bg_img)
img.place(x=0, y=0, relwidth=1, relheight=1)

# Creating Two canvas to show Input and Output Images
canvas = tk.Canvas(root,width = 650,height = 490,bg="lightgrey")
canvas.place(x=15,y=155)

canvas1 = tk.Canvas(root,width = 650,height = 490,bg="lightgrey")
canvas1.place(x=855,y=155)

app = App(root.master, root, "Object Detection")

# Create title label
title_lbl = tk.Label(root, text="Real-Time Object Detection using YOLO",font=("Lucida Bright", 34, "bold"),  bg="lightblue")
title_lbl.place(x=310, y=10)

# Create a label for Input Image
label1 = tk.Label(root, text="Input Image",font=("Lucida Bright", 20, "bold"), bg="yellow")
label1.place(x=260, y=100)

# Create a label for Output Image
label2 = tk.Label(root, text="Output Image",font=("Lucida Bright", 20, "bold"), bg="yellow")
label2.place(x=1120, y=100)

# Create a button to browse image
button = tk.Button(root, text="Browse Image", font=("Arial", 16, "bold"),bg="lightgreen",command = browse, height=1, width=12)
button.place(x=800, y=90)

# Create a button to show Input Image
button1 = tk.Button(root, text="Show Input Image", font=("Arial", 16, "bold"),bg="lightgreen",command = show, height=1, width=16)
button1.place(x=230, y=670)

# Create a button to show Output Image
button2 = tk.Button(root, text="Show Output Image", font=("Arial", 16, "bold"),bg="lightgreen",command = display, height=1, width=16)
button2.place(x=1100, y=670)

# Create a button to apply YOLO algorithm on the input image
button3 = tk.Button(root, text="Apply YOLO", font=("Arial", 16, "bold"),bg="lightgreen",command = run, height=1, width=12)
button3.place(x=680, y=400)

# Create a button to exit
button4 = tk.Button(root, text="Exit", font=("Arial", 16, "bold"),bg="orange",command = root.destroy, height=1, width=12)
button4.place(x=680, y=690)

root.mainloop()   