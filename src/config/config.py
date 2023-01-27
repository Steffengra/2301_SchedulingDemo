
import logging
from pathlib import (
    Path,
)
from sys import (
    stdout,
)
from numpy.random import (
    default_rng,
)
import tensorflow as tf

from src.data.user import (
    UserNormal,
    UserAmbulance,
)

# vergleich verschiedener ziele? maxminfair, max throughput, prio
# TODO: Figure out how to set priority


class Config:
    def __init__(
            self,
    ) -> None:

        # TODO: FIX THIS
        self.size_state: int = 5

        # GENERAL-------------------------------------------------------------------------------------------------------
        self._logging_level_stdio = logging.INFO  # DEBUG < INFO < WARNING < ERROR < CRITICAL
        self._logging_level_file = logging.INFO

        # SCHEDULING SIM PARAMETERS-------------------------------------------------------------------------------------
        self.snr_ue_linear: float = 1
        self.num_users: dict = {
            UserNormal: 2,
            UserAmbulance: 1,
        }
        self.max_job_size_resource_slots: dict = {
            'Normal': 5,
            'Ambulance': 5,
        }
        self.probs_new_job: dict = {
            'Normal': 0.8,
            'Ambulance': 0.5,
        }
        self.rayleigh_fading_scale: float = 1e-8
        self.total_resource_slots: int = 10

        self.reward_weightings = {
            'sum rate': 1.0,
            'priority missed': 1.0,
            'fairness': 1.0,
        }

        # LEARNING PARAMETERS-------------------------------------------------------------------------------------------
        self.experience_buffer_args: dict = {
            'buffer_size': 10_000,  # Num of samples held, FIFO
            'priority_scale_alpha': 0.0,  # alpha in [0, 1], alpha=0 uniform sampling, 1 is fully prioritized sampling
            'importance_sampling_correction_beta': 1.0  # beta in [0%, 100%], beta=100% is full correction
        }
        self.network_args: dict = {
            'value_network_args': {
                'hidden_layer_units': [512, 512, 512],
                'activation_hidden': 'tanh',  # >relu, tanh
                'kernel_initializer_hidden': 'glorot_uniform'  # >glorot_uniform, he_uniform
            },
            'value_network_optimizer': tf.keras.optimizers.Adam,
            'value_network_optimizer_args': {
                'learning_rate': 1e-4,
                # 'learning_rate': PiecewiseConstantDecay([int(0.8*self.num_episodes*200)], [1e-4, 1e-5]),
                'amsgrad': False,
            },

            'policy_network_args': {
                'hidden_layer_units': [512, 512, 512],
                'activation_hidden': 'tanh',  # >relu, tanh
                'kernel_initializer_hidden': 'glorot_uniform'  # >glorot_uniform, he_uniform
            },
            'policy_network_optimizer': tf.keras.optimizers.Adam,
            'policy_network_optimizer_args': {
                'learning_rate': 1e-4,
                # 'learning_rate': PiecewiseConstantDecay([int(0.8*self.num_episodes*200)], [1e-4, 1e-5]),
                'amsgrad': False,
            },

        }
        self.training_args: dict = {
            'training_minimum_experiences': 1_000,  # Min experiences collected before any training steps
            'training_batch_size': 256,  # Num of experiences sampled in one training step
            'training_target_update_momentum_tau': 1e-2,  # How much of the primary network copy to target networks
            'future_reward_discount_gamma': 0.0,  # Exponential future reward discount for stability

            'entropy_scale_alpha_initial': 1.0,  # Weights the 'soft' entropy penalty against the td error
            'target_entropy': 1.0,  # SAC heuristic impl. = product of action_space.shape
            'entropy_scale_optimizer': tf.keras.optimizers.SGD,
            'entropy_scale_optimizer_args': {
                'learning_rate': 1e-4,  # LR=0.0 -> No adaptive entropy scale -> manually tune initial entropy scale
            }
        }

        # POST INIT - DO NOT TOUCH--------------------------------------------------------------------------------------
        # Paths
        self.project_root_path = Path(__file__).parent.parent.parent

        # rng
        self.rng = default_rng(seed=None)

        # Logging
        #   get new sub loggers via logger.getChild(__name__) to improve messaging
        self.logger = logging.getLogger()

        self.logfile_path = Path(self.project_root_path, 'outputs', 'logs', 'log.txt')
        self.__logging_setup()

        # Collected args
        self.soft_actor_critic_args: dict = {
            'rng': self.rng,
            'parent_logger': self.logger,
            **self.training_args,
            'experience_buffer_args': {'rng': self.rng, **self.experience_buffer_args},
            'network_args': {**self.network_args, 'size_state': self.size_state, 'num_actions': len(self.num_users)},
        }

    def __logging_setup(
            self,
    ) -> None:
        logging_formatter = logging.Formatter(
            '{asctime} : {levelname:8s} : {name:30} : {funcName:20s} :: {message}',
            datefmt='%Y-%m-%d %H:%M:%S',
            style='{',
        )

        # Create Handlers
        logging_file_handler = logging.FileHandler(self.logfile_path)
        logging_stdio_handler = logging.StreamHandler(stdout)

        # Set Logging Level
        logging_file_handler.setLevel(self._logging_level_file)
        logging_stdio_handler.setLevel(self._logging_level_stdio)

        # Set Formatting
        logging_file_handler.setFormatter(logging_formatter)
        logging_stdio_handler.setFormatter(logging_formatter)
        self.logger.setLevel(logging.NOTSET)  # set logger level to lowest to catch all

        # Add Handlers
        self.logger.addHandler(logging_file_handler)
        self.logger.addHandler(logging_stdio_handler)

        # Check Log File Size
        large_log_file_size = 30_000_000
        if self.logfile_path.stat().st_size > large_log_file_size:
            self.logger.warning(f'log file size >{large_log_file_size/1_000_000} MB')
