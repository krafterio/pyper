# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).


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


def create_error(class_name, message: str):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        QueueJobError.__init__(self, message)

    new_class = type(class_name, (QueueJobError,), {'__init__': __init__})

    return new_class
