# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).


class QueueJobException(Exception):
    """Generic error managed by the queue jobs runner with traceback.
    """
    pass


class QueueJobError(QueueJobException):
    """Generic error managed by the queue jobs runner without traceback.
    """
    pass


class QueueJobProcessError(QueueJobError):
    """Error in process.
    """

    def __init__(self, message):
        """
        :param message: exception message and frontend exception info in job
        """
        super().__init__(message)
