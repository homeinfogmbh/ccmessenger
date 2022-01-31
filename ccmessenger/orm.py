"""Object-relational mappings."""

from __future__ import annotations
from datetime import datetime

from comcatlib import User
from mdb import Customer
from peewee import DateTimeField, ForeignKeyField, TextField

from peeweeplus import JSONModel, MySQLDatabaseProxy


__all__ = ['CustomerMessage', 'UserMessage']


DATABASE = MySQLDatabaseProxy('ccmessenger')


class CCMessengerModel(JSONModel):  # pylint: disable=R0903
    """Base model for this database."""

    class Meta:     # pylint: disable=R0903,C0115
        database = DATABASE
        schema = database.database


class Message(CCMessengerModel):
    """Common message base."""

    text = TextField()
    created = DateTimeField(default=datetime.now)


class CustomerMessage(Message):
    """A message from a customer to a user."""

    sender = ForeignKeyField(
        Customer, column_name='sender', on_delete='CASCADE', lazy_load=False
    )
    recipient = ForeignKeyField(
        User, column_name='recipient', on_delete='CASCADE', lazy_load=False
    )


class UserMessage(Message):
    """A message from a user to a customer."""

    sender = ForeignKeyField(
        User, column_name='sender', on_delete='CASCADE', lazy_load=False
    )
    recipient = ForeignKeyField(
        Customer, column_name='recipient', on_delete='CASCADE', lazy_load=False
    )
