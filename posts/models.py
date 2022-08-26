from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent = models.FloatField()
    received = models.FloatField()
    produced = models.FloatField()
    date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-date']
