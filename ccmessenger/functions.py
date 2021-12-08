"""Common functions."""

from typing import Optional, Union

from peewee import ModelSelect

from comcatlib import User
from filedb import File
from mdb import Address, Company, Customer, Tenement

from ccmessenger.orm import Message, Attachment


__all__ = [
    'get_customer_messages',
    'get_customer_message',
    'get_own_messages',
    'get_own_message',
    'get_user_messages',
    'get_user_message',
    'get_own_attachments',
    'get_own_attachment'
]


def get_customer_messages(customer: Union[Customer, int]) -> ModelSelect:
    """Selects messages of the given customer."""

    return Message.select(Message, Customer, Company, Attachment).join(
        Customer).join(Company).join_from(Message, User).join(
        Tenement).join_from(Message, Attachment).where(
        (Message.customer == customer)
        | (Tenement.customer == customer)
    )


def get_customer_message(ident: int, customer: Union[Customer, int]) \
        -> Message:
    """Returns a customer message."""

    return get_customer_messages(customer).where(Message.id == ident).get()


def get_own_messages(user: Union[User, int]) -> ModelSelect:
    """Selects messages of the given user."""

    return Message.select(Message, User, Tenement, Address, Attachment).join(
        User).join(Tenement).join(Address).join_from(
        Message, Attachment).where(
        (Message.user == user) & (Message.customer >> None))


def get_own_message(ident: int, user: Union[User, int]) -> Message:
    """Returns a user message."""

    return get_own_messages(user).where(Message.id == ident).get()


def get_user_messages(customer: Union[Customer, int], *,
                      user: Optional[Union[User, int]] = None) -> ModelSelect:
    """Selects user messages of the given customer."""

    condition = Tenement.customer == customer

    if user is None:
        condition &= Message.user == user

    return Message.select(Message, User, Tenement, Address, Attachment).join(
        User).join(Tenement).join(Address).join_from(
        Message, Attachment).where(condition)


def get_user_message(ident: int, customer: Union[Customer, int], *,
                     user: Optional[Union[User, int]] = None) -> Message:
    """Returns a user message of the give customer."""

    return get_user_messages(customer, user=user).where(
        Message.id == ident).get()


def get_own_attachments(user: Union[User, int]) -> Attachment:
    """Returns the respective attachment."""

    return Attachment.select(Attachment, Message, File).join(
        Message).join_from(Attachment, File).where(Message.user == user)


def get_own_attachment(ident: int, user: Union[User, int]) -> Attachment:
    """Returns the respective attachment."""

    return get_own_attachments(user).where(Attachment.id == ident).get()
