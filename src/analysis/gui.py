
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from numpy import (
    array,
)

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
)
from matplotlib.figure import Figure

from src.config.config import (
    Config,
)
from src.data.scheduling_data import (
    SchedulingData,
)


# CONFIG
label_img_width_scale = 0.1
label_img_height_scale = 0.1

label_img_logos_height = 0.07

button_font = ('Arial', 50)
button_user_width = 6  # relative to font size
button_user_height = 2  # relative to font size

label_resource_font = ('Arial', 50)
label_resource_width = 3  # relative to font size
label_resource_height = 1  # relative to font size

label_user_font = ('Arial', 25)

cp3: dict[str: str] = {  # uni branding
        'red1': '#9d2246',
        'red2': '#d50c2f',
        'red3': '#f39ca9',
        'blue1': '#00326d',
        'blue2': '#0068b4',
        'blue3': '#89b4e1',
        'purple1': '#3b296a',
        'purple2': '#8681b1',
        'purple3': '#c7c1e1',
        'peach1': '#d45b65',
        'peach2': '#f4a198',
        'peach3': '#fbdad2',
        'orange1': '#f7a600',
        'orange2': '#fece43',
        'orange3': '#ffe7b6',
        'green1': '#008878',
        'green2': '#8acbb7',
        'green3': '#d6ebe1',
        'yellow1': '#dedc00',
        'yellow2': '#f6e945',
        'yellow3': '#fff8bd',
        'white': '#ffffff',
        'black': '#000000',
    }

user_colors = {
    0: cp3['blue1'],
    1: cp3['blue2'],
    2: cp3['blue3'],
    3: cp3['red2'],
}

num_resources = 10


def get_height_rescale_constant_aspect_ratio(
        image: Image,
        new_height_px,
) -> int:
    new_width_px = int(new_height_px / image.height * image.width)
    return new_width_px


class App(tk.Tk):
    def __init__(
            self,
    ) -> None:
        super().__init__()
        self.configure(bg='white')
        self.attributes('-fullscreen', True)

        self.config = Config()

        # SIMS
        self.sim_main = SchedulingData(config=self.config)
        self.sim_0 = SchedulingData(config=self.config)
        self.sim_0.import_state(state=self.sim_main.export_state())

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

        label_img_height = int(label_img_height_scale * window_height)
        logo_img_height = int(label_img_logos_height * window_height)

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

        label_user_image_config = {
            'bg': 'white',
            'highlightthickness': 15,
        }

        label_user_text_config = {
            'font': label_user_font,
            'bg': 'white',
            'justify': tk.LEFT,
        }

        frames_config = {
            'bg': 'white',
            # 'relief': 'solid',
            # 'borderwidth': 2,
        }

        # GUI
        # Frames
        self.frame_scenario = tk.Frame(master=self, width=.5*window_width, height=.8*window_height, **frames_config)
        self.frame_scenario.place(relx=0.0)

        self.frame_resource_grid = tk.Frame(master=self, width=.2*window_width, height=.8*window_height, **frames_config)
        self.frame_resource_grid.place(relx=0.5)
        self.frame_resource_grid.pack_propagate(False)

        self.subframe_resource_grid = tk.Frame(master=self.frame_resource_grid, **frames_config)  # holds all the resource blocks in center of the resource grid frame
        self.subframe_resource_grid.pack(expand=True)

        self.frame_buttons = tk.Frame(master=self, width=.7*window_width, height=.2*window_height, **frames_config)
        self.frame_buttons.place(rely=0.8)
        self.frame_buttons.pack_propagate(False)

        self.frame_stats = tk.Frame(master=self, width=.3*window_width, height=1.0*window_height, **frames_config)
        self.frame_stats.place(relx=.7)
        self.frame_stats.pack_propagate(False)

        self.subframe_logos = tk.Frame(master=self.frame_scenario, **frames_config)
        self.subframe_logos.place(relx=0.0, rely=0.0)

        self.subframes_users = [
            tk.Frame(master=self.frame_scenario, **frames_config)
            for _ in range(4)
        ]
        self.subframes_users[0].place(relx=0.1, rely=0.2)
        self.subframes_users[1].place(relx=0.6, rely=0.15)
        self.subframes_users[2].place(relx=0.2, rely=0.7)
        self.subframes_users[3].place(relx=0.5, rely=0.6)

        # Logos
        self.images_logos = [
            Image.open('unilogo.png'),
            Image.open('ANT.png'),
        ]

        self.tk_image_logos = [
            ImageTk.PhotoImage(image_logo.resize((
                get_height_rescale_constant_aspect_ratio(image_logo, logo_img_height),
                logo_img_height,
            )))
            for image_logo in self.images_logos
        ]

        self.labels_img_logos = [
            tk.Label(self.subframe_logos, image=tk_image_logo, **label_user_text_config)
            for tk_image_logo in self.tk_image_logos
        ]

        for label_img_logo in self.labels_img_logos:
            label_img_logo.pack(side=tk.LEFT, padx=10, pady=10)

        # Users
        self.images_users = [
            Image.open('1.png'),
            Image.open('2.png'),
            Image.open('3.png'),
            Image.open('whambulance.png')
        ]

        self.tk_images_users = [
            ImageTk.PhotoImage(image_user.resize((
                get_height_rescale_constant_aspect_ratio(image_user, label_img_height),
                label_img_height,
            )))
            for image_user in self.images_users
        ]

        self.labels_img_users = [
            tk.Label(self.subframes_users[user_id],
                     image=self.tk_images_users[user_id],
                     highlightbackground=user_colors[user_id],
                     **label_user_image_config)
            for user_id in range(4)
        ]

        for label_img_user in self.labels_img_users:
            label_img_user.pack(anchor='w', pady=10)

        self.labels_text_users = [
            tk.Label(subframe_user, **label_user_text_config)
            for subframe_user in self.subframes_users
        ]

        self.update_user_text_labels()

        for label_text_user in self.labels_text_users:
            label_text_user.pack(anchor='w')

        # Buttons
        self.buttons_users = [
            tk.Button(self.frame_buttons, text='1', bg=user_colors[0], command=self.callback_button_user_0,
                      **button_user_config),
            tk.Button(self.frame_buttons, text='2', bg=user_colors[1], command=self.callback_button_user_1,
                      **button_user_config),
            tk.Button(self.frame_buttons, text='3', bg=user_colors[2], command=self.callback_button_user_2,
                      **button_user_config),
            tk.Button(self.frame_buttons, text='A', bg=user_colors[3], command=self.callback_button_user_ambulance,
                      **button_user_config),
        ]

        for button in self.buttons_users:
            button.pack(side=tk.LEFT, expand=True)

        # Resource Grid
        self.labels_resource_grid = [
            tk.Label(self.subframe_resource_grid, text='', **label_resource_config)
            for _ in range(num_resources)
        ]

        for label_resource_grid_id in range(len(self.labels_resource_grid)):
            self.labels_resource_grid[label_resource_grid_id].pack(side=tk.TOP)

        # Separator
        self.separator = ttk.Separator(orient='vertical')
        self.separator.place(relx=0.7, rely=0, relwidth=0.0, relheight=1)

        # Stats
        self.label_stats = tk.Label(self.frame_stats, text='this is a label for stats and such')
        self.label_stats.pack(side=tk.TOP)

        # FIG TEST
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        t = range(4)
        self.bars = ax.bar(t, [0, 0, 0, 0])
        ax.set_ylim([0, 1.0])

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_stats)  # A tk.DrawingArea.
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(side=tk.TOP)

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
            reward, reward_components = self.sim_main.step(percentage_allocation_solution=action)

            self.update_user_text_labels()

            for bar, value in zip(self.bars, action):
                bar.set_height(value)
            self.canvas.draw()
            self.current_resource_pointer = 0
            self.resources_per_user = {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
            }
            for label_resource in self.labels_resource_grid:
                label_resource.config(bg='white')

    def update_user_text_labels(
            self,
    ) -> None:
        for label_text_user_id, label_text_user in enumerate(self.labels_text_users):
            channel_strength = self.sim_main.users[label_text_user_id].power_gain
            if self.sim_main.users[label_text_user_id].job:
                resources = self.sim_main.users[label_text_user_id].job.size_resource_slots
            else:
                resources = 0
            text = f'Wants: {resources}\n' \
                   f'Channel Strength: {channel_strength}'
            label_text_user.configure(text=text)


if __name__ == '__main__':
    app = App()
    app.mainloop()
