class MetaInitError(Exception):
    pass


class ContextError(Exception):
    pass


class TaskError(Exception):
    pass


SINKER_ERROR_EXIST_MSG = 'Duplicate tasks already exist'


class SinkerError(Exception):
    pass
