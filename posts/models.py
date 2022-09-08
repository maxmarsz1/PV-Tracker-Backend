from django.db import models
from django.contrib.auth.models import User

import datetime


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_all = models.FloatField()
    received_all = models.FloatField()
    produced_all = models.FloatField()
    sent = models.FloatField(blank=True, default=0)
    received = models.FloatField(blank=True, default=0)
    produced = models.FloatField(blank=True, default=0)
    autoconsumption = models.FloatField(blank=True, default=0)
    consumption = models.FloatField(blank=True, default=0)

    date = models.DateField()
    

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')


    def save(self, *args, **kwargs):
        self.date = datetime.date(self.date.year, self.date.month, 1)
        all_posts = Post.objects.filter(user=self.user)

        #Setting previous month (and year if month was january)
        month, year = self.date.month - 1, self.date.year
        if month == 0:
            year -= 1
            month = 12
        
        #If there is post in this month already prevent saving
        if all_posts.get(date__year=self.date.year, date__month=self.date.month):
            pass

        try:
            previous_post = Post.objects.get(date__month=month, date__year=year, user=self.user)
            self.sent_month = self.sent - previous_post.sent
            self.received_month = self.received - previous_post.received
            self.produced_month = self.produced - previous_post.produced
            self.autoconsumption = self.produced - self.sent
            self.consumption = self.produced + self.received - self.sent

        #If there is no post in previous month we cannot calculate this month stats
        except Post.DoesNotExist as e:
            print('There is no post in previous month')
        except Exception as e:
            print(e)

        post = super(Post, self).save()


