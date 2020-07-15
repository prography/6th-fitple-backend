from __future__ import absolute_import, unicode_literals
from celery import shared_task
from config.email import send_application_notification_to_team_leader, \
    send_cancellation_of_application_confirmation_email_to_member, send_new_comment_notifications_email_to_team_leader, \
    send_new_child_comment_notifications_email_to_member, send_application_confirmation_email_to_member, \
    send_team_creation_confirmation_email_to_team_leader


# 호출 : def_email.delay(email)
# @shared_task
# def def_email(email):
#     print(email)
#     send_aplct_guide(email)
#     return True

# 2. 팀 생성 확인 : team_creation_confirmation_email_to_team_leader
@shared_task
def team_creation_email(email):
    send_team_creation_confirmation_email_to_team_leader(email)
    return True


# 3. 신청 확인 : application_confirmation_email_to_member
@shared_task
def application_confirmation_email(email):
    send_application_confirmation_email_to_member(email)
    return True


# 4. 신청 알림 : application_notification_to_team_leader
@shared_task
def application_notification_email(email):
    send_application_notification_to_team_leader(email)
    return True


# 5. 신청 취소 확인 : cancellation_of_application_confirmation_email_to_member
@shared_task
def cancellation_of_application_email(email):
    send_cancellation_of_application_confirmation_email_to_member(email)
    return True


# 7. 새 댓글 알림 : new_comment_notifications_email_to_team_leader
@shared_task
def new_comment_notifications_email(email, team_pk):
    send_new_comment_notifications_email_to_team_leader(email, team_pk)
    return True


# 8. 새 대댓글 알림 : new_child_comment_notifications_email_to_member
@shared_task
def new_child_comment_notifications_email(email, team_pk):
    send_new_child_comment_notifications_email_to_member(email, team_pk)
    return True
