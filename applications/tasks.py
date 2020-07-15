from celery import shared_task
from config.email import send_application_approval_notification_email_to_member, \
    send_application_refusal_notification_email_to_member


# # 호출 : def_email.delay()
# @shared_task
# def def_email():
#     send_test_email()
#     return True

# 승인, 거절
# 6. 신청 승인 알림 : send_application_approval_notification_email_to_member
@shared_task
def application_approval_email(email):
    send_application_approval_notification_email_to_member(email)
    return True

# 9. 신청 거절 알림 : send_application_refusal_notification_email_to_member
@shared_task
def application_refusal_email(email):
    send_application_refusal_notification_email_to_member(email)
    return True
