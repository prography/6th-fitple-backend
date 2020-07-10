from django.db import models


# Create your models here.

class Feedback(models.Model):
    feedback = models.TextField('피드벡')
