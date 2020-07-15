from __future__ import absolute_import, unicode_literals
from celery import shared_task
from config.email import send_test_email, send_welcome_to_member

# 호출 : def_email.delay()
@shared_task
def def_email():
    send_test_email()
    return True

# welcome
@shared_task
def def_welcome_email(email):
    send_welcome_to_member(email)
    return True
