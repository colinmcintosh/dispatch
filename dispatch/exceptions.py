

# Exception messages
EXC_DOT_IN_NAME = "'name' parameter may not contain a '.' symbol."
EXC_COLON_IN_NAME = "'name' parameter may not contain a ':' symbol."
EXC_NOT_PROFILE_OBJECT = "'{}' is not an instance of the Profile class."


class DispatchException(Exception):
    pass


class DispatchSyntaxException(DispatchException):
    pass


class DispatchProfileNotFound(DispatchException):
    pass


class DispatchNoProfileMatched(DispatchException):
    pass


class DispatchMissingParameter(DispatchException):
    pass
