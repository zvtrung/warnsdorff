import Image
import ImageDraw
import ImageTk
import subprocess
import sys
import Tkinter

def next_frame(label, im, draw):
    line = sys.stdin.readline().rstrip()
    if not line:
        return
    data = eval(line)
    fill = "red" if data["tiebreak"] else "blue"
    draw.point(data["square"], fill = fill)

    frame = ImageTk.PhotoImage(im) 
    label.config(image=frame)
    label.image = frame
    label.pack()   
    label.master.after(1, next_frame, label, im, draw)

n = int(sys.argv[1])

im = Image.new("RGB", (n, n))
draw = ImageDraw.Draw(im)
draw.rectangle((0, 0, n, n), fill="white")

root = Tkinter.Tk()
frame = ImageTk.PhotoImage(im)
label = Tkinter.Label(root, image=frame)
label.pack()
root.after(1, next_frame, label, im, draw)
root.mainloop()