"""Common error handlers."""

from wsgilib import JSONMessage

from ccmessenger.orm import CustomerMessage, UserMessage


__all__ = ["ERRORS"]


ERRORS = {
    CustomerMessage.DoesNotExist: lambda _: JSONMessage(
        "No such customer message.", status=404
    ),
    UserMessage.DoesNotExist: lambda _: JSONMessage(
        "No such user message.", status=404
    ),
}
