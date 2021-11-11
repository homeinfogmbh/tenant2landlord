"""Tenant-to-tenant messaging ORM models."""

from __future__ import annotations
from datetime import datetime
from typing import Union

from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import TextField

from hwdb import Deployment
from mdb import Address, Customer
from notificationlib import get_email_orm_model
from peeweeplus import MySQLDatabase, JSONModel

from tenant2landlord.config import CONFIG


__all__ = ['TenantMessage', 'NotificationEmail']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class _Tenant2LandlordModel(JSONModel):     # pylint: disable=R0903
    """Basic model for this database."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


class TenantMessage(_Tenant2LandlordModel):
    """Tenant to landlord messages."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'tenant_message'

    customer = ForeignKeyField(Customer, column_name='customer')
    address = ForeignKeyField(Address, column_name='address')
    message = TextField()
    created = DateTimeField(default=datetime.now)
    read = BooleanField(default=False)

    @classmethod
    def add(cls, customer: Union[Customer, int], address: Union[Address, int],
            message: str):
        """Creates a new entry for the respective customer and address."""
        record = cls()
        record.customer = customer
        record.address = address
        record.message = message
        return record

    @classmethod
    def from_deployment(cls, deployment: Union[Deployment, int],
                        message: str) -> TenantMessage:
        """Creates a new entry for the respective deployment."""
        return cls.add(deployment.customer, deployment.address, message)

    def to_json(self, address: bool = True, **kwargs) -> dict:
        """Adds the address to the dictionary."""
        json = super().to_json(**kwargs)

        if address:
            json['address'] = self.address.to_json()

        return json


NotificationEmail = get_email_orm_model(_Tenant2LandlordModel)
