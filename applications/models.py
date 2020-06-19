from django.contrib.auth import get_user_model
from django.db import models

from teams.models import Team

User = get_user_model()


class TeamApplication(models.Model):
    DEVELOPER, PLANNER, DESIGNER = 'Developer', 'Planner', 'Designer'
    APPROVED, REJECTED, CANCELED, WAITING = 'Approved', 'Rejected', 'Canceled', 'Waiting'
    JOB_CHOICES = [
        (DEVELOPER, 'Developer'),
        (PLANNER, 'Planner'),
        (DESIGNER, 'Designer'),
    ]
    JOIN_STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELED, 'Canceled'),
        (WAITING, 'Waiting'),
    ]
    # team  applicant  join_status  job  created_at
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  #
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)  #

    join_status = models.CharField(
        max_length=10,
        choices=JOIN_STATUS_CHOICES,
        default=WAITING
    )  # 지원상태
    job = models.CharField(  #
        max_length=10,
        choices=JOB_CHOICES,
        default=DEVELOPER
    )  # 직무

    created_at = models.DateField('신청생성시간', auto_now_add=True)


class JoinQuestions(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    question1 = models.TextField(default='안녕하세요! 간단한 자기소개 부탁드립니다!')
    question2 = models.TextField(default='팀에 지원하는 동기는 무엇인가요?')  # 잘 되는지 test !!
    question3 = models.TextField(default='팀의 어떤 부분에 기여하고 싶으신가요? 다양한 생각을 들려주세요!')


class JoinAnswers(models.Model):
    application = models.ForeignKey(TeamApplication, on_delete=models.CASCADE)

    answer1 = models.TextField()
    answer2 = models.TextField()
    answer3 = models.TextField()
