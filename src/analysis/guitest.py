
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


def callback_button_user_1():
    pass


def callback_button_user_2():
    pass


def callback_button_user_3():
    pass


def callback_button_user_ambulance():
    pass




label_img_width_scale = 0.1
label_img_height_scale = 0.1

bg_user_1 = 'blue'
bg_user_2 = 'yellow'
bg_user_3 = 'green'
bg_user_ambulance = 'red'

window = tk.Tk()
window.configure(bg='white')
window.attributes('-fullscreen', True)
window_width = window.winfo_screenwidth()
window_height = window.winfo_screenheight()

img_user_1 = ImageTk.PhotoImage(
    Image.open('1.png').resize(
        (int(label_img_width_scale*window_width), int(label_img_height_scale*window_height))
    )
)

img_user_2 = ImageTk.PhotoImage(
    Image.open('2.png').resize(
        (int(label_img_width_scale*window_width), int(label_img_height_scale*window_height))
    )
)

img_user_3 = ImageTk.PhotoImage(
    Image.open('3.png').resize(
        (int(label_img_width_scale*window_width), int(label_img_height_scale*window_height))
    )
)

img_user_ambulance = ImageTk.PhotoImage(
    Image.open('whambulance.png').resize(
        (int(label_img_width_scale*window_width), int(label_img_height_scale*window_height))
    )
)

label_img_user_1 = tk.Label(window, image=img_user_1, bg=bg_user_1)
label_img_user_2 = tk.Label(window, image=img_user_2, bg=bg_user_2)
label_img_user_3 = tk.Label(window, image=img_user_3, bg=bg_user_3)
label_img_user_ambulance = tk.Label(window, image=img_user_ambulance, bg=bg_user_ambulance)

label_img_user_1.grid(row=0, column=0)
label_img_user_2.grid(row=0, column=1)
label_img_user_3.grid(row=1, column=0)
label_img_user_ambulance.grid(row=1, column=1)

button_user_1 = tk.Button(window, text='1', bg=bg_user_1, command=callback_button_user_1)
button_user_2 = tk.Button(window, text='2', bg=bg_user_2, command=callback_button_user_2)
button_user_3 = tk.Button(window, text='3', bg=bg_user_3, command=callback_button_user_3)
button_user_ambulance = tk.Button(window, text='A', bg=bg_user_ambulance, command=callback_button_user_ambulance)

button_user_1.grid(row=3, column=0)
button_user_2.grid(row=3, column=1)
button_user_3.grid(row=3, column=2)
button_user_ambulance.grid(row=3, column=3)

separator = ttk.Separator(orient='vertical')
separator.place(relx=0.7, rely=0, relwidth=0.0, relheight=1)

window.mainloop()
