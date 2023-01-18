
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

        # INITIALIZE RESOURCE GRID
        self.resource_grid = ResourceGrid(total_resource_slots=self.config.total_resource_slots)
        self.logger.info('ResourceGrid initialized')

        # INITIALIZE USERS
        self.users = []
        user_id = 0
        for user_type, user_type_amount in self.config.num_users.items():
            for user_type_idx in range(user_type_amount):
                self.users.append(user_type(user_id=user_id, parent_logger=self.logger))
                user_id += 1
        self.logger.info('Users initialized')



        self.logger.info('SchedulingData sim initialized')

    def step(
            self,
            action,
    ) -> None:

        # Calculate Action results -> Reward
        reward = None

        return reward
