from django.core.mail.message import EmailMessage


def send_email():
    print("send email test start2")
    subject = "이메일 테스트2"
    to = ['lemontech119@gmail.com']
    from_email = 'fitple.dev@gmail.com'
    message = "email test가 성공했습니다.2"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
