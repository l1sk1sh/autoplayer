"""Few exceptions that are used for DST
"""


class Error(Exception):
    """Base class for other exceptions"""
    pass


class SteamLoginException(Error):
    """Raised when code failed to login to Steam account"""
    pass


class ApplicationFailedToStart(Error):
    """Raised when check for running application failed"""

    def __init__(self, application):
        self.application = application


class ApplicationFailedToOpen(Error):
    """Raised when focus on app has failed"""

    def __init__(self, application):
        self.application = application


class MenuIsNotReached(Error):
    """Raised when for some reason, main menu has not been loaded"""
    pass
