"""Object-relational mappings."""

from __future__ import annotations
from datetime import datetime

from comcatlib import User
from filedb import File
from mdb import Customer
from peewee import DateTimeField, ForeignKeyField, TextField

from peeweeplus import JSONModel, MySQLDatabaseProxy


__all__ = ['Message', 'Attachment']


DATABASE = MySQLDatabaseProxy('ccmessenger')


class CCMessengerModel(JSONModel):  # pylint: disable=R0903
    """Base model for this database."""

    class Meta:     # pylint: disable=R0903,C0115
        database = DATABASE
        schema = database.database


class Message(CCMessengerModel):
    """A Message."""

    parent = ForeignKeyField('self', column_name='parent', null=True)
    user = ForeignKeyField(User, column_name='user', null=True,
                           on_delete='CASCADE', lazy_load=False)
    customer = ForeignKeyField(Customer, column_name='customer', null=True,
                               on_delete='CASCADE', lazy_load=False)
    text = TextField()
    created = DateTimeField(default=datetime.now)

    @classmethod
    def for_user(cls, user: User, text: str) -> Message:
        """Creates a message for the given user."""
        return cls(user=user, text=text)

    @classmethod
    def for_customer(cls, customer: Customer, text: str) -> Message:
        """Creates a message for the given customer."""
        return cls(customer=customer, text=text)


class Attachment(CCMessengerModel):     # pylint: disable=R0903
    """A file attachment."""

    message = ForeignKeyField(Message, column_name='message',
                              backref='attachments', on_delete='CASCADE')
    file = ForeignKeyField(File, column_name='file')
