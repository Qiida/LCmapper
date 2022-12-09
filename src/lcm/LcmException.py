def raiseInputOutputException():
    try:
        raise LcmIOException
    except LcmIOException as exception:
        print(exception)


def raiseMissingDataException(lcm):
    try:
        raise LcmMissingDataException(lcm=lcm)
    except LcmException as exception:
        print(exception)


class LcmException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class LcmIOException(LcmException):
    def __init__(self, message="lcm.IOException: Either file or path."):
        super().__init__(message)


class LcmMissingDataException(LcmException):
    def __init__(self, lcm, message="lcm.MissingDataException"):
        super().__init__(message)
