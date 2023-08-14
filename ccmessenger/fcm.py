"""Firebase Cloud Messaging API."""

from logging import getLogger
from firebase_admin.messaging import BatchResponse

from comcatlib.fcm import APP_NAME
from comcatlib.fcm import CAPTIONS
from comcatlib.fcm import URLCode
from comcatlib.fcm import get_tokens
from comcatlib.fcm import multicast_message

from ccmessenger.orm import CustomerMessage


__all__ = ["notify"]


def notify(customer_message: CustomerMessage) -> BatchResponse:
    """Multicast customer message to users."""

    getLogger("ccmessenger").info(
        "Notifying about customer message: %s", customer_message
    )

    # TODO: Add caption for UrlCode.CONTACT as soon as ComCat app provides a
    #  respective name.
    try:
        title = CAPTIONS[URLCode.CONTACT]
    except KeyError:
        return BatchResponse([])

    return multicast_message(
        [token.token for token in get_tokens({customer_message.recipient})],
        url_code=URLCode.EVENTS,
        title=f"{APP_NAME}: {title}",
        body=customer_message.text,
    )
