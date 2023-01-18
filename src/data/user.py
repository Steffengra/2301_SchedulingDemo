
from logging import Logger


class _User:
    def __init__(
            self,
            user_id: int,
            user_type: str,
            parent_logger: Logger
    ) -> None:

        # SETUP
        self.logger = parent_logger.getChild(f'{__name__}_{user_id}')

        self.user_id: int = user_id
        self.user_type: str = user_type

        self.power_gain_db: float = None

        self.logger.info(f'User {user_id} type {user_type} initialized')


class UserNormal(_User):
    def __init__(
            self,
            user_id: int,
            parent_logger: Logger,
    ) -> None:

        _User.__init__(
            self,
            user_id=user_id,
            user_type='Normal',
            parent_logger=parent_logger,
        )


class UserAmbulance(_User):
    def __init__(
            self,
            user_id: int,
            parent_logger: Logger,
    ) -> None:

        _User.__init__(
            self,
            user_id=user_id,
            user_type='Ambulance',
            parent_logger=parent_logger,
        )
