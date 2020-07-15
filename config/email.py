from django.core.mail.message import EmailMessage, EmailMultiAlternatives

from rest_framework import settings

from config.settings import development

FROM_EMAIL = development.EMAIL_HOST_USER


def send_test_email():
    subject = "이메일 테스트2"

    # to = ['lemontech119@gmail.com']
    to = ['dqgsh1055@gmail.com']
    # from_email = 'fitple.dev@gmail.com'

    # message = "email test\n가 성공했습니다.\n2" # <p></p>
    message = '''<html><body>
    <p>모집해주신 프로젝트에 <br>
    지원자가 있습니다</p>
    <p>https://fit-ple.com/ 에서 확인해주세요!</p>
    <p>김시현</p>
    </body></html>
    '''
    # "모집해주신 프로젝트에 지원자가 있습니다.\nhttps://fit-ple.com/ 에서 확인해주세요!<br/><br/><br/>김시현"

    # EmailMessage(subject=subject, body=message, to=to, from_email=FROM_EMAIL).send()

    # msg = EmailMessage(subject=subject, body=message, to=to, from_email=FROM_EMAIL)
    # msg.content_subtype = "html"  # Main content is now text/html
    # msg.send()

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# def send_aplct_guide(email):
#     email_list = []
#     email_list.append(email)
#     subject = "(Fit-ple) 모집중인 프로젝트에 지원가 있습니다."
#     to = email_list
#     # from_email = 'fitple.dev@gmail.com'
#     message = "모집해주신 프로젝트에 지원자가 있습니다.\nhttps://fit-ple.com/ 에서 확인해주세요!"
#     EmailMessage(subject=subject, body=message, to=to, from_email=FROM_EMAIL).send()


# def 이메일_전송_템플릿(email):
#     # to = ['dqgsh1055@gmail.com']
#     to = [email]
#
#     subject = ""
#     # <p></p> <br>
#     message = '''<html><body>
#     <p></p>
#     </body></html>
#     ''' + COMMON_MESSAGES
#
#     msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
#     msg.attach_alternative(message, "text/html")
#     msg.send()


# : 수신인 : member team_member team_leader

# 1. 가입 환영-본인 : send_welcome_to_member
# 2. 팀 생성 확인-본인 : team_creation_confirmation_email_to_team_leader
# 3. 신청 확인-본인 : application_confirmation_email_to_member
# 4. 신청 알림-팀장 : application_notification_to_team_leader
# 5. 신청 취소 확인-본인 : cancellation_of_application_confirmation_email_to_member
# 6. 신청 승인 알림-팀원 : application_approval_notification_email_to_member
# 7. 새 댓글 알림-팀장 : new_comment_notifications_email_to_team_leader
# 8. 새 대댓글 알림-댓글주인 : new_child_comment_notifications_email_to_member
# 9. 신청 거절 알림-회원 : application_refusal_notification_email_to_member

##
# ok 1. 가입 환영 : send_welcome_to_member
def send_welcome_to_member(email):
    subject = "(Fit-ple) 가입해주셔서 감사합니다!"
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    message = '''<html><body>
        <p>마이페이지에서 프로필 정보 추가 입력하시면 <br>
        보다 더 Fit이 맞는 팀원을 <br>
        찾을 수 있다는 사실, 아시나요?</p>
        <p>Fitple, 많은 이용바랍니다!</p>
        <p>메일 수신거부 설정은 마이페이지에서 가능합니다. <br>
        https://fit-ple.com/</p>        
        </body></html>
        '''

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# <p></p> <br>
COMMON_MESSAGES = '''
<p>이용해주셔서 감사합니다!</p>
<p>Fitple, 어떠신가요? <br>
  소중한 피드백 주신다면 곧 바로 반영해보겠습니다! <br>
  https://fit-ple.com/feedback</p>
<p>메일 수신거부 설정은 마이페이지에서 가능합니다. <br>
https://fit-ple.com/</p>
'''


# 2. 팀 생성 확인 : team_creation_confirmation_email_to_team_leader
def send_team_creation_confirmation_email_to_team_leader(email):
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    subject = "(Fit-ple) 팀이 생성되었습니다!"
    # <p></p> <br>
    message = '''<html><body>
    <p>팀장님과 Fit이 맞는 팀원들을 찾길 바랍니다! <br>
항상 응원하고 있어요!</p>
        </body></html>
        ''' + COMMON_MESSAGES

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# 3. 신청 확인 : application_confirmation_email_to_member
def send_application_confirmation_email_to_member(email):
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    subject = "(Fit-ple) 팀 지원 확인 메일입니다."
    # <p></p> <br>
    message = '''<html><body>
    <p>지원해주셔서 감사합니다. <br>
  지원 결과는 메일을 통해 알려드립니다.  <br>
  마이페이지에서도 확인하실 수 있습니다!</p>
        </body></html>
        ''' + COMMON_MESSAGES

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# 4. 신청 알림 : application_notification_to_team_leader
def send_application_notification_to_team_leader(email):
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    subject = "(Fit-ple) 팀 지원 내역이 있습니다."
    # <p></p> <br>
    message = '''<html><body>
        <p>생성하신 팀에 지원자가 있습니다! <br>
  마이페이지에서 지원 내용을 확인하고, Fit이 맞는 팀원과 함께 하세요!</p>
        </body></html>
        ''' + COMMON_MESSAGES

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# 5. 신청 취소 확인 : send_cancellation_of_application_confirmation_email_to_member
def send_cancellation_of_application_confirmation_email_to_member(email):
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    subject = "(Fit-ple) 팀 지원 취소 확인 메일입니다."
    # <p></p> <br>
    message = '''<html><body>
        <p>팀 지원이 취소되었습니다. <br>
  Fit이 맞지 않을까봐 고민이시군요! <br>
  Fitple이 더 노력하겠습니다!</p>
        </body></html>
        ''' + COMMON_MESSAGES

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# ok 6. 신청 승인 알림 : send_application_approval_notification_email_to_member
def send_application_approval_notification_email_to_member(email):
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    subject = "(Fit-ple) 팀 지원이 승인되었습니다!"
    # <p></p> <br>
    message = '''<html><body>
        <p>축하드립니다! <br>
  Fit이 맞는 팀원을 찾으셨군요! <br>
  꾸준히 참여하여 멋진 서비스를 완성해보세요!</p>
        <p>승인 내역은 마이페이지에서 확인하실 수 있습니다. <br>
  곧 팀장이 공지 메일을 발송할거에요! <br>
  조금 기다려주세요!</p>
        </body></html>
        ''' + COMMON_MESSAGES

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# 7. 새 댓글 알림 : send_new_comment_notifications_email_to_team_leader
def send_new_comment_notifications_email_to_team_leader(email, team_pk):
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    subject = "(Fit-ple) 팀 모집 페이지에 댓글이 있습니다."
    # <p></p> <br>
    message = '''<html><body>
        <p>모집하시는 내용에 궁금한 분이 계신가봐요! <br>
  혹시 Fit이 맞는 팀원일까요?</p>
        </body></html>
        ''' + COMMON_MESSAGES

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# 8. 새 대댓글 알림 : send_new_child_comment_notifications_email_to_member
def send_new_child_comment_notifications_email_to_member(email, team_pk):
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    subject = "(Fit-ple) 작성하신 댓글에 대댓글이 있습니다."
    # <p></p> <br>
    message = '''<html><body>
        <p>작성하신 댓글에 댓글이 달렸나봐요!</p>
        </body></html>
        ''' + COMMON_MESSAGES

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()


# ok 9. 신청 거절 알림 : send_application_refusal_notification_email_to_member
def send_application_refusal_notification_email_to_member(email):
    # to = ['dqgsh1055@gmail.com']
    to = [email]

    subject = "(Fit-ple) 팀 지원이 거절되었습니다."
    # <p></p> <br>
    message = '''<html><body>
        <p>회원님과 Fit이 맞는 팀은 아니었나봐요! <br>
  다른 팀을 찾아보거나 <br>
  직접 Fit이 맞는 팀원들을 모집해보세요!</p>
        <p>지원 내역은 마이페이지에서 확인하실 수 있습니다.</p>
        </body></html>
        ''' + COMMON_MESSAGES

    msg = EmailMultiAlternatives(subject=subject, body="text_content", from_email=FROM_EMAIL, to=to)
    msg.attach_alternative(message, "text/html")
    msg.send()

