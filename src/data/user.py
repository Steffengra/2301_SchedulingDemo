
from logging import Logger
from numpy.random import Generator

from src.data.job import (
    Job,
)


class _User:
    def __init__(
            self,
            user_id: int,
            user_type: str,
            max_job_sizes_resource_slots: dict,
            rayleigh_fading_scale: float,
            probs_new_job: dict,
            rng: Generator,
            parent_logger: Logger
    ) -> None:

        # SETUP
        self.rng = rng
        self.logger = parent_logger.getChild(f'{__name__}_{user_id}')

        self.user_id: int = user_id
        self.user_type: str = user_type

        self.max_job_size_resource_slots: int = max_job_sizes_resource_slots[self.user_type]

        self.rayleigh_fading_scale = rayleigh_fading_scale
        self.power_gain: float = 0.0
        self.update_power_gain()

        self.job = None
        self.prob_new_job: float = probs_new_job[self.user_type]

        self.logger.info(f'User {user_id} type {user_type} initialized')

    def update_power_gain(
            self,
    ) -> None:

        # fading = self.rng.rayleigh(scale=self.rayleigh_fading_scale)
        # fading = self.rng.integers(low=1, high=1)
        fading = 1
        self.power_gain = fading ** 2


        self.logger.debug(f'User {self.user_id} type {self.user_type} power gain updated to {self.power_gain}')

    def generate_job(
            self,
    ) -> None:

        size_resource_slots = self.rng.integers(low=1, high=self.max_job_size_resource_slots + 1)
        job = Job(size_resource_slots=size_resource_slots)
        self.job = job


class UserNormal(_User):
    def __init__(
            self,
            user_id: int,
            max_job_sizes_resource_slots: dict,
            rayleigh_fading_scale: float,
            probs_new_job: dict,
            rng: Generator,
            parent_logger: Logger,
    ) -> None:

        _User.__init__(
            self,
            user_id=user_id,
            user_type='Normal',
            max_job_sizes_resource_slots=max_job_sizes_resource_slots,
            rayleigh_fading_scale=rayleigh_fading_scale,
            probs_new_job=probs_new_job,
            rng=rng,
            parent_logger=parent_logger,
        )


class UserAmbulance(_User):
    def __init__(
            self,
            user_id: int,
            max_job_sizes_resource_slots: dict,
            rayleigh_fading_scale: float,
            probs_new_job: dict,
            rng: Generator,
            parent_logger: Logger,
    ) -> None:

        _User.__init__(
            self,
            user_id=user_id,
            user_type='Ambulance',
            max_job_sizes_resource_slots=max_job_sizes_resource_slots,
            rayleigh_fading_scale=rayleigh_fading_scale,
            probs_new_job=probs_new_job,
            rng=rng,
            parent_logger=parent_logger,
        )
