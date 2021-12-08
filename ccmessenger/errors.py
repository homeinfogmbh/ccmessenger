"""Common error handlers."""

from wsgilib import JSONMessage

from ccmessenger.orm import Attachment, Message


__all__ = ['ERRORS']


ERRORS = {
    Attachment.DoesNotExist: lambda _: JSONMessage(
        'No such attachment.', status=404),
    Message.DoesNotExist: lambda _: JSONMessage(
        'No such message.', status=404)
}
