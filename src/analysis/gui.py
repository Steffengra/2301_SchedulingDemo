
from pathlib import Path
from sys import path as sys_path

project_root_path = Path(Path(__file__).parent, '..', '..')
sys_path.append(str(project_root_path.resolve()))

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

import numpy as np

from src.config.config import (
    Config,
)
from src.config.config_gui import (
    ConfigGUI,
)
from src.data.scheduling_data import (
    SchedulingData,
)
from src.analysis.gui_elements import (
    Scenario,
    ScreenSelector,
    ScreenResults,
    ScreenStats,
)
from src.utils.get_width_rescale_constant_aspect_ratio import get_width_rescale_constant_aspect_ratio


class App(tk.Tk):

    def __init__(
            self,
    ) -> None:

        super().__init__()
        self.configure(bg='white')
        self.attributes('-fullscreen', True)

        self.config = Config()
        self.config_gui = ConfigGUI()

        self.window_width = self.winfo_screenwidth()
        self.window_height = self.winfo_screenheight()

        self.countdown_toggle = False
        self.countdown_value = 0

        # SIMS
        self.sim_main = SchedulingData(config=self.config)
        self.secondary_simulations = {
            learner_name: SchedulingData(config=self.config)
            for learner_name in self.config_gui.learned_agents.keys()
        }
        self.update_secondary_simulations()

        self.resources_per_user = {
            user_id: 0
            for user_id in range(4)
        }

        # LIFETIME STATS
        self.lifetime_stats = {
            'self': {
                'sumrate': [],
                'fairness': [],
                'timeouts': [],
                'overall': [],
            }
        }
        for learner_name in self.config_gui.learned_agents.keys():
            self.lifetime_stats[learner_name] = {
                'sumrate': [],
                'fairness': [],
                'timeouts': [],
                'overall': [],
            }
        self.maximum_reward_achieved = 0.1

        # ARITHMETIC
        self.channel_img_height = int(self.config_gui.label_user_font[1]*1.2)
        self.label_base_station_height = int(self.config_gui.label_img_base_station_height_scale * self.window_height)

        self._gui_setup()

    def _gui_setup(
            self,
    ) -> None:

        self.images_channelstrength = [
            Image.open(Path(project_root_path, 'src', 'analysis', 'img', 'low.png')),
            Image.open(Path(project_root_path, 'src', 'analysis', 'img', 'medlow.png')),
            Image.open(Path(project_root_path, 'src', 'analysis', 'img', 'medhigh.png')),
            Image.open(Path(project_root_path, 'src', 'analysis', 'img', 'high.png')),
        ]
        self.tk_images_channel_strength = [
            ImageTk.PhotoImage(image_channel_strength.resize((
                get_width_rescale_constant_aspect_ratio(image_channel_strength, self.channel_img_height),
                self.channel_img_height,
            )))
            for image_channel_strength in self.images_channelstrength
        ]

        # Scenario - left hand side of the screen
        self.frame_scenario = Scenario(
            master=self,
            config_gui=self.config_gui,
            window_width=self.window_width,
            window_height=self.window_height,
            logo_paths=[Path(project_root_path, 'src', 'analysis', 'img', logo) for logo in self.config_gui.logos],
            user_image_paths=[Path(project_root_path, 'src', 'analysis', 'img', user_image) for user_image in self.config_gui.user_images],
            base_station_image_path=Path(project_root_path, 'src', 'analysis', 'img', self.config_gui.base_station_image),
            button_callbacks=[self.callback_button_user_0, self.callback_button_user_1, self.callback_button_user_2, self.callback_button_user_ambulance],
            num_total_resource_slots=self.config.num_total_resource_slots,
            **self.config_gui.frames_config,
        )

        # Screen selector buttons - top right of screen
        self.frame_screen_selector = ScreenSelector(
            master=self,
            config_gui=self.config_gui,
            window_width=self.window_width,
            window_height=self.window_height,
            button_commands=[self.change_to_frame_allocations, self.change_to_frame_stats],
            **self.config_gui.frames_config
        )

        # Results - bottom right hand side of screen, switched via screen selector buttons
        self.frame_results = ScreenResults(
            master=self,
            config_gui=self.config_gui,
            window_width=self.window_width,
            window_height=self.window_height,
            num_total_resource_slots=self.config.num_total_resource_slots,
            **self.config_gui.frames_config
        )

        # Stats - bottom right hand side of screen, switched via selector buttons
        self.frame_stats = ScreenStats(
            master=self,
            window_height=self.window_height,
            window_width=self.window_width,
            config_gui=self.config_gui,
            button_timer_image_path=Path(project_root_path, 'src', 'analysis', 'img', self.config_gui.button_panic_img),
            button_timer_callback=self.callback_button_timer,
            **self.config_gui.frames_config
        )

        # Place frames
        self.frame_scenario.place(relx=0.0)

        self.frame_screen_selector.place(relx=.7)
        self.frame_screen_selector.pack_propagate(False)

        self.frame_results.place(relx=.7, rely=.1)
        self.frame_results.pack_propagate(False)

        self.frame_stats.place(relx=.7, rely=0.1)
        self.frame_stats.pack_propagate(False)

        # Separator Vertical
        self.separator_vertical = ttk.Separator(self, orient='vertical')
        self.separator_vertical.place(relx=0.7, rely=0, relwidth=0.0, relheight=1)

        self.selectable_frames = {
            'AllocationResults': self.frame_stats,
            'Stats': self.frame_results,
        }

        self.update_user_text_labels()

    def check_loop(
            self,
    ) -> None:

        if self.countdown_toggle:
            if self.countdown_value == 0:
                self.evaluate_allocation()
                self.countdown_value = self.config_gui.countdown_reset_value_seconds

            self.countdown_value -= 1
            self.frame_stats.button_timer.configure(text=f'{self.countdown_value}', image=self.frame_stats.pixel)  # workaround so button doesn't resize on click
            self.after(1000, self.check_loop)

    def change_to_frame_allocations(
            self,
    ) -> None:

        for frame in self.selectable_frames.values():
            self.frame_results.tkraise(aboveThis=frame)

    def change_to_frame_stats(
            self,
    ) -> None:

        for frame in self.selectable_frames.values():
            self.frame_stats.tkraise(aboveThis=frame)

    def callback_button_timer(
            self,
    ) -> None:

        self.countdown_toggle = not self.countdown_toggle
        if self.countdown_toggle:
            self.countdown_value = self.config_gui.countdown_reset_value_seconds
            self.after(1000, self.check_loop)

        if not self.countdown_toggle:
            self.frame_stats.button_timer.configure(text='', image=self.frame_stats.tk_image_stopwatch)

    def callback_button_user_0(
            self,
            event,
    ) -> None:
        self.allocate_resource(user_id=0)

    def callback_button_user_1(
            self,
            event,
    ) -> None:
        self.allocate_resource(user_id=1)

    def callback_button_user_2(
            self,
            event,
    ) -> None:
        self.allocate_resource(user_id=2)

    def callback_button_user_ambulance(
            self,
            event,
    ) -> None:
        self.allocate_resource(user_id=3)

    def allocate_resource(
            self,
            user_id,
    ) -> None:

        current_resource_pointer = self.frame_scenario.resource_grid.allocate(color=self.config_gui.user_colors[user_id])

        self.resources_per_user[user_id] += 1
        if current_resource_pointer == self.config.num_total_resource_slots:
            self.after(100, self.evaluate_allocation)

    def evaluate_allocation(
            self,
    ) -> None:

        # get own action
        action = np.array(list(self.resources_per_user.values())) / self.config.num_total_resource_slots
        action = action.astype('float32')
        self.frame_results.resource_grids[self.config_gui.allocator_names[0]].fill(
            allocation=self.get_allocated_slots(percentage_allocation_solution=action, sim=self.sim_main),
            color_dict=self.config_gui.user_colors,
        )
        reward, reward_components = self.sim_main.step(percentage_allocation_solution=action)

        instant_stats = [[
            reward_components['sum rate'],
            reward_components['fairness score'],
            reward_components['prio jobs missed'],
            reward
        ]]

        self.lifetime_stats['self']['sumrate'].append(reward_components['sum rate'])
        self.lifetime_stats['self']['fairness'].append(reward_components['fairness score'])
        self.lifetime_stats['self']['timeouts'].append(reward_components['prio jobs missed'])
        self.lifetime_stats['self']['overall'].append(reward)

        # get learner actions
        for learner_name, learner in self.config_gui.learned_agents.items():
            action = learner.call(self.secondary_simulations[learner_name].get_state()[np.newaxis]).numpy().squeeze()
            self.frame_results.resource_grids[self.config_gui.learned_agents_display_names[learner_name]].fill(
                allocation=self.get_allocated_slots(percentage_allocation_solution=action, sim=self.secondary_simulations[learner_name]),
                color_dict=self.config_gui.user_colors,
            )

            reward, reward_components = self.secondary_simulations[learner_name].step(percentage_allocation_solution=action)

            instant_stats.append(
                [
                    reward_components['sum rate'],
                    reward_components['fairness score'],
                    reward_components['prio jobs missed'],
                    reward
                ]
            )

            self.lifetime_stats[learner_name]['sumrate'].append(reward_components['sum rate'])
            self.lifetime_stats[learner_name]['fairness'].append(reward_components['fairness score'])
            self.lifetime_stats[learner_name]['timeouts'].append(reward_components['prio jobs missed'])
            self.lifetime_stats[learner_name]['overall'].append(reward)

        self.update_user_text_labels()

        mean_rewards = [np.mean(self.lifetime_stats[member]['overall']) for member in self.lifetime_stats.keys()]
        self.frame_stats.lifetime_stats.update(values=mean_rewards)

        # reset resources
        self.resources_per_user = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
        }
        self.frame_scenario.resource_grid.clear()

        self.countdown_value = self.config_gui.countdown_reset_value_seconds
        self.update_secondary_simulations()

        # Update instant stats
        self.frame_stats.instant_stats.clear()
        self.frame_results.instant_stats.clear()
        instant_stats = np.round(np.array(instant_stats), 1)

        cmaps = [
            self.config_gui.fig_lifetime_stats_gradient_cmap,  # sumrate
            self.config_gui.fig_lifetime_stats_gradient_cmap,  # fairness
            self.config_gui.fig_lifetime_stats_gradient_cmap_reversed,  # deaths
            self.config_gui.fig_lifetime_stats_gradient_cmap,  # overall
        ]
        colors = [[[0, 0, 0, 0] for _ in range(4)] for _ in range(4)]
        for column_index, cmap in enumerate(cmaps):

            column_stats = instant_stats[:, column_index].copy()
            column_stats += min(column_stats)  # transform to positive space
            if max(column_stats) > 0:
                column_stats = column_stats / max(column_stats)  # transform to [0, 1]

            # set color map
            column_colors = cmap(column_stats)

            for column_color_id, column_color in enumerate(column_colors):
                colors[column_color_id][column_index] = list(column_color)

        self.frame_stats.instant_stats.draw_instant_stats_table(data=instant_stats, colors=colors, **self.config_gui.fig_instant_stats_config)
        self.frame_results.instant_stats.draw_instant_stats_table(data=instant_stats, colors=colors, **self.config_gui.fig_instant_stats_config)

    def get_channel_strength_image(
            self,
            channel_strength,
    ) -> tk.PhotoImage:

        if channel_strength >= 16:
            return self.tk_images_channel_strength[3]
        if channel_strength >= 9:
            return self.tk_images_channel_strength[2]
        if channel_strength >= 3:
            return self.tk_images_channel_strength[1]
        if channel_strength >= 1:
            return self.tk_images_channel_strength[0]

        raise ValueError('Unexpected channel strength')

    def update_user_text_labels(
            self,
    ) -> None:

        # Resource Wants
        for label_text_user_id, frame_user in enumerate(self.frame_scenario.frames_users):
            if self.sim_main.users[label_text_user_id].job:
                resources = self.sim_main.users[label_text_user_id].job.size_resource_slots
            else:
                resources = 0
            text = f'Wants: {resources} Resources'
            frame_user.label_user_text_wants.configure(
                text=text
            )

        # Channel Strength
        for label_text_user_id, frame_user in enumerate(self.frame_scenario.frames_users):
            channel_strength = self.sim_main.users[label_text_user_id].power_gain
            text = 'Channel: '
            frame_user.label_user_text_channel_strength.configure(
                text=text,
                image=self.get_channel_strength_image(channel_strength),
                compound=tk.RIGHT,
            )

    def update_secondary_simulations(
            self,
    ) -> None:

        for sec_sim in self.secondary_simulations.values():
            sec_sim.import_state(state=self.sim_main.export_state())

    def get_allocated_slots(
            self,
            percentage_allocation_solution: np.ndarray,
            sim,
    ):
        requested_slots_per_ue = [
            sim.users[ue_id].job.size_resource_slots if sim.users[ue_id].job else 0
            for ue_id in range(len(sim.users))
        ]

        slot_allocation_solution = [
            np.minimum(
                np.round(percentage_allocation_solution[ue_id] * self.config.num_total_resource_slots),
                requested_slots_per_ue[ue_id],
                dtype='float32'
            )
            for ue_id in range(len(sim.users))
        ]

        # grant at most one additional resource if there was rounding down
        if sum(slot_allocation_solution) == sim.resource_grid.total_resource_slots - 1:
            remainders = np.round([
                percentage_allocation_solution[ue_id] * sim.resource_grid.total_resource_slots - slot_allocation_solution[ue_id]
                for ue_id in range(len(sim.users))
            ], decimals=5)
            for ue_id in range(len(sim.users)):
                if remainders[ue_id] > 0:
                    if requested_slots_per_ue[ue_id] > slot_allocation_solution[ue_id]:
                        slot_allocation_solution[ue_id] += 1
                        break

        # Check if the rounding has resulted in more resources distributed than available
        if sum(slot_allocation_solution) > sim.resource_grid.total_resource_slots:
            # if so, remove one resource from a random user
            while sum(slot_allocation_solution) > sim.resource_grid.total_resource_slots:
                random_user_id = self.config.rng.integers(0, len(sim.users))
                if slot_allocation_solution[random_user_id] > 0:
                    slot_allocation_solution[random_user_id] -= 1

        # prepare the allocated slots per ue for metrics calculation
        allocated_slots_per_ue: dict = {
                ue_id: slot_allocation_solution[ue_id]
                for ue_id in range(len(sim.users))
        }

        return allocated_slots_per_ue


if __name__ == '__main__':
    app = App()
    app.mainloop()
