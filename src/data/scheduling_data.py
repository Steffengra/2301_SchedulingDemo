
from numpy import (
    log2,
    multiply,
    mean,
    std,
)

from src.data.resource_grid import (
    ResourceGrid,
)


class SchedulingData:
    def __init__(
            self,
            config,
    ) -> None:

        self.config = config
        self.logger = self.config.logger.getChild(__name__)
        self.rng = self.config.rng

        # INITIALIZE RESOURCE GRID
        self.resource_grid = ResourceGrid(total_resource_slots=self.config.total_resource_slots)
        self.logger.info('ResourceGrid initialized')

        # INITIALIZE USERS
        self.users = {}
        user_id = 0
        for user_type, user_type_amount in self.config.num_users.items():
            for user_type_idx in range(user_type_amount):
                self.users[user_id] = (
                    user_type(
                        user_id=user_id,
                        max_job_sizes_resource_slots=self.config.max_job_size_resource_slots,
                        rayleigh_fading_scale=self.config.rayleigh_fading_scale,
                        probs_new_job=self.config.probs_new_job,
                        rng=self.rng,
                        parent_logger=self.logger
                    )
                )
                user_id += 1
        self.logger.info('Users initialized')

        self.generate_new_jobs()
        self.logger.info('SchedulingData sim initialized')

    def generate_new_jobs(
            self,
    ) -> None:

        for user in self.users.values():
            if self.rng.random() < self.config.job_creation_probability:
                user.generate_job()

    def update_user_power_gain(
            self,
    ) -> None:

        for user in self.users.values():
            user.update_power_gain()

    def step(
            self,
            percentage_allocation_solution,
    ) -> tuple[dict, dict]:

        # figure out how many resource slots each user actually gets based on allocation solution
        allocated_slots_per_ue = {
            0: 1,
            1: 1,
            2: 1,
        }

        # calculate sum rate
        sum_rate_capacity_kbit_per_second: float = 0.0
        for user_id, allocated_slots in allocated_slots_per_ue.items():
            sum_rate_capacity_kbit_per_second += (
                allocated_slots * log2(1 + self.users[user_id].power_gain * self.config.snr_ue_linear) / 1_000
            )

        self.logger.debug(f'sum rate {sum_rate_capacity_kbit_per_second}')

        # see how many priority==1 jobs were not fully transmitted
        priority_jobs_missed_counter: int = 0
        for user_id in allocated_slots_per_ue.keys():
            if self.users[user_id].job.priority == 1:
                if allocated_slots_per_ue[user_id] < self.users[user_id].job.size_resource_slots:
                    priority_jobs_missed_counter += 1

        self.logger.debug(f'prio jobs missed {priority_jobs_missed_counter}')

        # calculate jain's fairness score
        #  result ranges from 1/n (worst) to 1.0 (best)
        power_gains = [user.power_gain for user in self.users.values()]
        weighted_slots_per_ue = multiply(list(allocated_slots_per_ue.values()), power_gains)
        fairness_score = 1 / (
                1 + (std(weighted_slots_per_ue) / mean(weighted_slots_per_ue))**2
        )

        # transform to [0.. 1]?
        fairness_score = (fairness_score - 1/len(self.users)) / (1 - 1/len(self.users))

        self.logger.debug(f'weighted slots per ue {weighted_slots_per_ue}')
        self.logger.debug(f'fairness_score {fairness_score}')

        reward = (
            + self.config.reward_weightings['sum rate'] * sum_rate_capacity_kbit_per_second
            + self.config.reward_weightings['priority missed'] * priority_jobs_missed_counter
            + self.config.reward_weightings['fairness'] * fairness_score
        )

        reward_components = {
            'sum rate': sum_rate_capacity_kbit_per_second,
            'prio jobs missed': priority_jobs_missed_counter,
            'weighted slots per ue': weighted_slots_per_ue,
            'fairness score': fairness_score,
        }

        # move sim to new state
        self.update_user_power_gain()
        self.generate_new_jobs()

        return reward, reward_components
