"""Emailing of new tenant-to-tenant messages."""

from typing import Iterator

from emaillib import EMail
from functoolsplus import coerce
from notificationlib import get_email_func

from tenant2landlord.config import CONFIG
from tenant2landlord.orm import NotificationEmail, TenantMessage


__all__ = ['email']


@coerce(frozenset)
def get_emails(message: TenantMessage) -> Iterator[EMail]:
    """Yields notification emails."""

    for notification_email in NotificationEmail.select().where(
            NotificationEmail.customer == message.customer):
        recipient = notification_email.email
        subject = notification_email.subject or CONFIG['email']['subject']
        subject = subject.format(address=message.address)
        sender = CONFIG['email']['from']
        html = message.message if notification_email.html else None
        plain = None if notification_email.html else message.message
        yield EMail(subject, sender, recipient, plain=plain, html=html)


email = get_email_func(get_emails)  # pylint: disable=C0103
