class NotFound(RuntimeError):
    pass


# When something has no value set yet.
class NotSet(RuntimeError):
    pass


class RemoteSubmitFailed(RuntimeError):
    pass


class CapacityReached(RuntimeError):
    pass


class DuplicateLabelException(RuntimeError):
    pass


class DuplicateUuidException(RuntimeError):
    pass


class DlsXchemBeflowClientConnectorError(RuntimeError):
    pass


class Factory:
    def build(qualname):
        if qualname == "soakdb3_api.exceptions.CapacityReached":
            return CapacityReached
        return None
