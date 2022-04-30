from discord.errors import DiscordException

__all__ = (
    "GenericError",
    "AuthorNotInVoice",
    "NoVoiceClient",
    "BadArgument",
    "BadAttachment",
    "NoAttachment",
    "EmptyQueue"
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


class TimeoutError(GenericError):
    def __init__(self, msg="Couldn't find an image"):

