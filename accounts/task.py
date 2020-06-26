from __future__ import absolute_import, unicode_literals
from celery import shared_task
from config.email import send_email


@shared_task
def def_email():
    send_email()
    return True
