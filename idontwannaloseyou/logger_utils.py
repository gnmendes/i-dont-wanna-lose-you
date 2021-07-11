import logging


class LoggerFactory(object):

    @staticmethod
    def get_logger(instance_name,
                   log_level=logging.DEBUG,
                   log_file=None):

        logging.basicConfig(level=log_level, filename=log_file)
        return logging.getLogger(instance_name)
