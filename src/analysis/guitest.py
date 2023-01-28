
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from numpy import (
    array,
)


# CONFIG
label_img_width_scale = 0.1
label_img_height_scale = 0.1

button_font = ('Helvetica', 50)
button_user_width = 6  # relative to font size
button_user_height = 2  # relative to font size

label_resource_font = ('Helvetica', 50)
label_resource_width = 3  # relative to font size
label_resource_height = 1  # relative to font size

user_colors = {
    0: 'blue',
    1: 'yellow',
    2: 'green',
    3: 'red',
}

num_resources = 10


class App(tk.Tk):
    def __init__(
            self,
    ) -> None:
        super().__init__()
        self.configure(bg='white')
        self.attributes('-fullscreen', True)

        self.current_resource_pointer = 0
        self.resources_per_user = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
        }

        # ARITHMETIC
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        label_img_width = int(label_img_width_scale * window_width)
        label_img_height = int(label_img_height_scale * window_height)

        button_user_config = {
            'font': button_font,
            'width': button_user_width,
            'height': button_user_height,
        }

        label_resource_config = {
            'font': label_resource_font,
            'width': label_resource_width,
            'height': label_resource_height,
            'borderwidth': 2,
            'relief': 'solid',
            'bg': 'white',
        }

        # GUI
        self.frame_scenario = tk.Frame(master=self, borderwidth=2, relief='solid', bg='grey', width=.5*window_width, height=.8*window_height)
        self.frame_scenario.place(relx=0.0)

        self.frame_resource_grid = tk.Frame(master=self, borderwidth=2, relief='solid', bg='grey', width=.2*window_width, height=.8*window_height)
        self.frame_resource_grid.place(relx=0.5)
        self.frame_resource_grid.pack_propagate(False)

        self.subframe_resource_grid = tk.Frame(master=self.frame_resource_grid)  # holds all the resource blocks in center of the resource grid frame
        self.subframe_resource_grid.pack(expand=True)

        self.frame_buttons = tk.Frame(master=self, borderwidth=2, relief='solid', bg='grey', width=.7*window_width, height=.2*window_height)
        self.frame_buttons.place(rely=0.8)
        self.frame_buttons.pack_propagate(False)

        self.frame_stats = tk.Frame(master=self, borderwidth=2, relief='solid', bg='grey', width=.3*window_width, height=1.0*window_height)
        self.frame_stats.place(relx=.7)

        img_user_0 = ImageTk.PhotoImage(
            Image.open('1.png').resize(
                (int(label_img_width_scale*window_width), int(label_img_height_scale*window_height))
            )
        )

        img_user_1 = ImageTk.PhotoImage(
            Image.open('2.png').resize(
                (int(label_img_width_scale*window_width), int(label_img_height_scale*window_height))
            )
        )

        img_user_2 = ImageTk.PhotoImage(
            Image.open('3.png').resize(
                (int(label_img_width_scale*window_width), int(label_img_height_scale*window_height))
            )
        )

        img_user_ambulance = ImageTk.PhotoImage(
            Image.open('whambulance.png').resize(
                (int(label_img_width_scale*window_width), int(label_img_height_scale*window_height))
            )
        )

        self.label_img_user_0 = tk.Label(self.frame_scenario, image=img_user_0, bg=user_colors[0])
        self.label_img_user_1 = tk.Label(self.frame_scenario, image=img_user_1, bg=user_colors[1])
        self.label_img_user_2 = tk.Label(self.frame_scenario, image=img_user_2, bg=user_colors[2])
        self.label_img_user_ambulance = tk.Label(self.frame_scenario, image=img_user_ambulance, bg=user_colors[3])

        # label_img_user_1.grid(row=0, column=0)
        # label_img_user_2.grid(row=0, column=1)
        # label_img_user_3.grid(row=1, column=0)
        # label_img_user_ambulance.grid(row=1, column=1)

        button_user_0 = tk.Button(self.frame_buttons, text='1', bg=user_colors[0], command=self.callback_button_user_0, **button_user_config)
        button_user_1 = tk.Button(self.frame_buttons, text='2', bg=user_colors[1], command=self.callback_button_user_1, **button_user_config)
        button_user_2 = tk.Button(self.frame_buttons, text='3', bg=user_colors[2], command=self.callback_button_user_2, **button_user_config)
        button_user_ambulance = tk.Button(self.frame_buttons, text='A', bg=user_colors[3], command=self.callback_button_user_ambulance, **button_user_config)
        self.buttons_user = [button_user_0, button_user_1, button_user_2, button_user_ambulance]

        for button in self.buttons_user:
            button.pack(side=tk.LEFT, expand=True)

        self.labels_resource_grid = [tk.Label(self.subframe_resource_grid, text='', **label_resource_config)
                                for resource_id in range(num_resources)]

        for label_resource_grid_id in range(len(self.labels_resource_grid)):
            self.labels_resource_grid[label_resource_grid_id].pack(side=tk.TOP)

        self.separator = ttk.Separator(orient='vertical')
        self.separator.place(relx=0.7, rely=0, relwidth=0.0, relheight=1)

        self.label_stats = tk.Label(self.frame_stats, text='this is a label for stats and such')
        self.label_stats.pack()

    def callback_button_user_0(
            self,
    ) -> None:
        self.allocate_resource(user_id=0)

    def callback_button_user_1(
            self,
    ) -> None:
        self.allocate_resource(user_id=1)

    def callback_button_user_2(
            self,
    ) -> None:
        self.allocate_resource(user_id=2)

    def callback_button_user_ambulance(
            self,
    ) -> None:
        self.allocate_resource(user_id=3)

    def allocate_resource(
            self,
            user_id,
    ) -> None:
        self.labels_resource_grid[self.current_resource_pointer].config(bg=user_colors[user_id])
        self.current_resource_pointer = self.current_resource_pointer + 1
        self.resources_per_user[user_id] += 1
        if self.current_resource_pointer == num_resources:
            action = array(list(self.resources_per_user.values())) / num_resources
            action = action.astype('float32')
            # TODO: DO SOMETHING
            print(action)
            self.current_resource_pointer = 0
            self.resources_per_user = {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
            }
            for label_resource in self.labels_resource_grid:
                label_resource.config(bg='white')


if __name__ == '__main__':
    app = App()
    app.mainloop()
