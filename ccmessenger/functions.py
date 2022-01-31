"""Common functions."""

from typing import Optional, Union

from peewee import JOIN, Select

from comcatlib import User
from mdb import Address, Company, Customer, Tenement

from ccmessenger.orm import CustomerMessage, UserMessage


__all__ = [
    'get_customer_messages',
    'get_customer_message',
    'get_user_messages',
    'get_user_message'
]


def get_customer_messages(
        sender: Union[Customer, int], *,
        recipient: Optional[Union[User, int]] = None
) -> Select:
    """Selects messages of the given customer."""

    condition = CustomerMessage.sender == sender

    if recipient is not None:
        condition &= CustomerMessage.recipient == recipient

    return CustomerMessage.select(CustomerMessage, Customer, Company).join(
        Customer, JOIN.LEFT_OUTER).join(Company, JOIN.LEFT_OUTER).join_from(
        CustomerMessage, User).join(Tenement).where(condition)


def get_customer_message(
        ident: int, sender: Union[Customer, int], *,
        recipient: Optional[Union[User, int]] = None
) -> CustomerMessage:
    """Returns a customer message."""

    return get_customer_messages(sender, recipient=recipient).where(
        CustomerMessage.id == ident).get()


def get_user_messages(sender: Union[User, int]) -> Select:
    """Selects messages of the given user."""

    return UserMessage.select(UserMessage, User, Tenement, Address).join(
        User).join(Tenement).join(Address).where(UserMessage.sender == sender)


def get_user_message(ident: int, sender: Union[User, int]) -> UserMessage:
    """Returns a user message."""

    return get_user_messages(sender).where(UserMessage.id == ident).get()
