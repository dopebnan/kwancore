from discord.errors import DiscordException

__all__ = (
    "GenericError",
    "AuthorNotInVoice",
    "NoVoiceClient",
    "BadArgument",
    "BadAttachment",
    "NoAttachment",
    "EmptyQueue",
    "ItemNotFound"
)


class GenericError(DiscordException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class VoiceClientError(GenericError):
    pass


class AuthorNotInVoice(VoiceClientError):
    def __init__(self, message="Author not in any voice channel"):
        super().__init__(message)


class NoVoiceClient(VoiceClientError):
    def __init__(self, message="Bot isn't in any voice channel"):
        super().__init__(message)


class EmptyQueue(VoiceClientError):
    pass


class BadArgument(GenericError):
    def __init__(self, message, arg):
        self.message = message
        super().__init__(f"'{arg}' -> {message}")


class BadAttachment(BadArgument):
    pass


class NoAttachment(GenericError):
    pass


class RoleError(GenericError):
    def __init__(self, role, author):
        super().__init__(f"'{role}' not in '{author}'.roles")


class MoneyError(GenericError):
    pass


class ProfileAlreadyExists(MoneyError):
    def __init__(self, user, msg=None):
        msg = msg or f"{user} already has a profile"
        super().__init__(msg)


class ProfileNotFound(MoneyError):
    def __init__(self, user, msg=None):
        msg = msg or f"{user}'s profile doesn't exist, you can make one via `kc!money_start`"
        super().__init__(msg)


class ItemNotFound(MoneyError):
    pass
