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
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='applications')  #
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


class JoinQuestion(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='questions')
    # team 에서 여기 접근할 때 questions 이름으로 ?

    question = models.TextField()


class JoinAnswer(models.Model):
    application = models.ForeignKey(TeamApplication, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(JoinQuestion, on_delete=models.CASCADE)

    answer = models.TextField()
