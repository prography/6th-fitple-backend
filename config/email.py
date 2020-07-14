from django.core.mail.message import EmailMessage
from rest_framework import settings

from config.settings import development

FROM_EMAIL = development.EMAIL_HOST_USER


def send_test_email():
    subject = "이메일 테스트2"
    to = ['lemontech119@gmail.com']
    # from_email = 'fitple.dev@gmail.com'

    message = "email test가 성공했습니다.2"
    EmailMessage(subject=subject, body=message, to=to, from_email=FROM_EMAIL).send()


def send_aplct_guide(email):
    email_list = []
    email_list.append(email)
    subject = "(Fit-ple) 모집중인 프로젝트에 지원가 있습니다."
    to = email_list
    # from_email = 'fitple.dev@gmail.com'
    message = "모집해주신 프로젝트에 지원자가 있습니다.\nhttps://fit-ple.com/ 에서 확인해주세요!"
    EmailMessage(subject=subject, body=message, to=to, from_email=FROM_EMAIL).send()