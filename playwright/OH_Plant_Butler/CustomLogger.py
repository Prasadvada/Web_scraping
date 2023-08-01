import logging
import sys
from common import create_folder_if_not_exists

log_format = "%(asctime)s:%(msecs)03d: %(name)s: %(levelname)s: %(message)s"
log_date_format = "%m/%d/%Y %I:%M:%S"


class LogGen:
    """
    Class creates custom loggers, defines file and database handler also

    """

    @staticmethod
    def log_gen(file_path: str, file_name: str, db_name: str = 'sample.db', job_id: int = 0) -> logging.Logger:
        create_folder_if_not_exists(file_path)
        log_file_path = f"{file_path}/{file_name}_Logs.log"
        logging.basicConfig(filename=log_file_path, format=log_format, datefmt=log_date_format, filemode='w')

        # logger = logging.getLogger(file_name)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(LogGen.add_file_handler())
        return logger

    @staticmethod
    def add_file_handler():
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(log_format, datefmt=log_date_format)
        handler.setFormatter(formatter)
        return handler
