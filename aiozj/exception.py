
class AioZjError(Exception):
    pass


class AioZjTimeoutError(AioZjError):
    pass


class AioZjAuthError(AioZjError):
    pass

