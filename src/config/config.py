
import logging
from pathlib import (
    Path,
)
from sys import (
    stdout,
)

from src.data.user import (
    UserNormal,
    UserAmbulance,
)

# vergleich verschiedener ziele? maxminfair, max throughput, prio


class Config:
    def __init__(
            self,
    ) -> None:

        # GENERAL
        self._logging_level_stdio = logging.INFO  # DEBUG < INFO < WARNING < ERROR < CRITICAL
        self._logging_level_file = logging.INFO

        # SCHEDULING SIM PARAMETERS
        self.num_users: dict = {
            UserNormal: 2,
            UserAmbulance: 1,
        }
        self.total_resource_slots: int = 5

        # LEARNING PARAMETERS


        # OTHER SETUP
        self.project_root_path = Path(__file__).parent.parent.parent

        # logging
        #   get new sub loggers via logger.getChild(__name__) to improve messaging
        self.logger = logging.getLogger()

        self.logfile_path = Path(self.project_root_path, 'outputs', 'logs', 'log.txt')
        self.logging_setup()

    def logging_setup(
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
