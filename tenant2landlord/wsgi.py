"""Authenticated and authorized HIS services."""

from typing import Union

from flask import request
from peewee import ModelSelect

from his import CUSTOMER, authenticated, authorized, Application
from mdb import Customer
from notificationlib import get_wsgi_funcs
from wsgilib import JSON, JSONMessage

from tenant2landlord.orm import TenantMessage, NotificationEmail


__all__ = ['APPLICATION']


APPLICATION = Application('Tenant-to-landlord', debug=True)
ALLOWED_PATCH_FIELDS = {'message', 'read'}
SKIPPED_PATCH_FIELDS = {
    key for key, *_ in TenantMessage.get_json_fields()
    if key not in ALLOWED_PATCH_FIELDS
}


def _get_messages(customer: Union[Customer, int]) -> ModelSelect:
    """Yields the customer's tenant-to-landlord messages."""

    return TenantMessage.select().where(TenantMessage.customer == customer)


def _get_message(ident: int) -> TenantMessage:
    """Returns the respective message."""

    try:
        return TenantMessage.get(
            (TenantMessage.id == ident)
            & (TenantMessage.customer == CUSTOMER.id))
    except TenantMessage.DoesNotExist:
        raise JSONMessage('The requested message does not exist.',
                          status=404) from None


@authenticated
@authorized('tenant2landlord')
def list_messages() -> JSON:
    """Lists the tenant-to-landlord messages."""

    return JSON([message.to_json() for message in _get_messages(CUSTOMER.id)])


@authenticated
@authorized('tenant2landlord')
def get_message(ident: int) -> JSON:
    """Returns the respective message of the customer."""

    return JSON(_get_message(ident).to_json())


@authenticated
@authorized('tenant2landlord')
def toggle_message(ident: int) -> JSONMessage:
    """Toggles the respective message."""

    message = _get_message(ident)
    message.read = not message.read
    message.save()
    return JSONMessage('The message has been toggled.', read=message.read,
                       status=200)


@authenticated
@authorized('tenant2landlord')
def patch_message(ident: int) -> JSONMessage:
    """Toggles the respective message."""

    message = _get_message(ident)
    message.patch_json(request.json, skip=SKIPPED_PATCH_FIELDS)
    message.save()
    return JSONMessage('The message has been updated.', status=200)


@authenticated
@authorized('tenant2landlord')
def delete_message(ident: int) -> JSONMessage:
    """Deletes the respective message."""

    message = _get_message(ident)
    message.delete_instance()
    return JSONMessage('The message has been deleted.', status=200)


GET_EMAILS, SET_EMAILS = get_wsgi_funcs('tenant2landlord', NotificationEmail)


APPLICATION.add_routes((
    ('GET', '/message', list_messages),
    ('GET', '/message/<int:ident>', get_message),
    ('PUT', '/message/<int:ident>', toggle_message),
    ('PATCH', '/message/<int:ident>', patch_message),
    ('DELETE', '/message/<int:ident>', delete_message),
    ('GET', '/email', GET_EMAILS),
    ('POST', '/email', SET_EMAILS)
))
