class ProcrastiNOTorError(Exception):
    __cause__: str = "No cause provided"
    __suppress_context__: bool = False
    __traceback__ = __cause__

class NoWastersError(ProcrastiNOTorError):
    __cause__ = "No wasters provided"

class HugeWastersCountError(ProcrastiNOTorError):
    __cause__ = "Too much wasters provided. Keep it under 100"

class NoTimeLimitError(ProcrastiNOTorError):
    __cause__ = "No time limit provided"

class IncorrectTimeLimitTypeError(ProcrastiNOTorError):
    __cause__ = "Incorrect time limit type. It must be a number"

class HugeTimeLimitValueError(ProcrastiNOTorError):
    __cause__ = "Too big time limit value. It must be less than a day"


ProcrastiNOTorErrors: tuple = (NoWastersError, HugeWastersCountError, NoTimeLimitError, IncorrectTimeLimitTypeError,
                             HugeTimeLimitValueError)
