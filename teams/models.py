from django.db import models
from accounts.models import User
from config.storage_backends import PublicMediaStorage
from config.utils import s3_test_image_upload_to


# Create your models here.
## Tag는 나중에...
# class Tag(models.Model):
#     name = models.CharField(max_length=10, primary_key=True)
#
#     def __str__(self):
#         return self.name


class Team(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=100)
    # tags = models.ManyToManyField(Tag, related_name='teams', verbose_name='태그', blank=True)
    description = models.TextField('설명')
    # status = models.CharField('상태', max_length=20)
    planner = models.PositiveIntegerField('기획자', default=0)
    developer = models.PositiveIntegerField('개발자', default=0)
    designer = models.PositiveIntegerField('디자이너', default=0)
    region = models.CharField('지역', max_length=20)
    goal = models.CharField('목표', max_length=10)
    # kind = models.CharField('종류', max_length=40) #
    # people = models.CharField('사용고객', max_length=20) #
    image = models.FileField('이미지',
                             upload_to=s3_test_image_upload_to,
                             storage=PublicMediaStorage(),
                             default='default_team.jpg')
    created_at = models.DateTimeField('생성시간', auto_now_add=True)
    modified_at = models.DateTimeField('수정시간', auto_now=True)

    RECRUITMENT_IN_PROGRESS, RECRUITMENT_DEADLINE, IN_ACTIVITY, END_OF_ACTIVITY = '모집진행중', '모집마감', '활동중', '활동종료'
    ACTIVE_STATUS_CHOICES = [
        (RECRUITMENT_IN_PROGRESS, '모집진행중'),
        (RECRUITMENT_DEADLINE, '모집마감'),
        (IN_ACTIVITY, '활동중'),
        (END_OF_ACTIVITY, '활동종료'),
    ]
    active_status = models.CharField(
        max_length=15,
        choices=ACTIVE_STATUS_CHOICES,
        default=RECRUITMENT_IN_PROGRESS
    )
    # recruitment_deadline = models.CharField(max_length=15, default='0000-00-00') #

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=100)
    created_at = models.DateTimeField('생성시간', auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

# class Question(models.Model):
#     team = models.ForeignKey(Team, related_name='questions', on_delete=models.CASCADE)
#     first_question = models.CharField(max_length=100, null=True)
#     second_question = models.CharField(max_length=100, null=True)
#     third_question = models.CharField(max_length=100, null=True)
