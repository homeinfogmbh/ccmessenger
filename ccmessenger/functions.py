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
    'get_user_messages',
    'get_user_message',
    'get_attachment'
]


def get_customer_messages(customer: Union[Customer, int], *,
                          user: Optional[Union[User, int]] = None
                          ) -> ModelSelect:
    """Selects messages of the given customer."""

    condition = Message.customer == customer

    if user is not None:
        condition &= Message.user == user

    return Message.select(Message, Customer, Company, Attachment).join(
        Customer).join(Company).join_from(Message, User).join(
        Tenement).join_from(Message, Attachment).where(condition)


def get_customer_message(ident: int, customer: Union[Customer, int], *,
                         user: Optional[Union[User, int]] = None) -> Message:
    """Returns a customer message."""

    return get_customer_messages(customer, user=user).where(
        Message.id == ident).get()


def get_user_messages(user: Union[User, int], *,
                      own: bool = False) -> ModelSelect:
    """Selects messages of the given user."""

    condition = Message.user == user

    if own:
        condition &= Message.customer >> None

    return Message.select(Message, User, Tenement, Address, Attachment).join(
        User).join(Tenement).join(Address).join_from(
        Message, Attachment).where(condition)


def get_user_message(ident: int, user: Union[User, int], *,
                     own: bool = False) -> Message:
    """Returns a user message."""

    return get_user_messages(user, own=own).where(Message.id == ident).get()


def get_attachment(ident: int, *,
                   customer: Optional[Union[Customer, int]] = None,
                   user: Optional[Union[User, int]] = None,
                   own: bool = False) -> ModelSelect:
    """Returns the respective attachment."""

    condition = Attachment.id == ident

    if customer is not None:
        condition &= Message.customer == customer
    elif own:
        condition &= Message.customer >> None

    if user is not None:
        condition &= Message.user == user

    return Attachment.select(Attachment, File).join(Attachment, File).where(
        condition).get()
