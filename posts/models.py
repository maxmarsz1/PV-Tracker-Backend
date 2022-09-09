from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .utils import calculate_month

import datetime
from dateutil import relativedelta


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produced_all = models.FloatField()
    received_all = models.FloatField()
    sent_all = models.FloatField()
    produced = models.FloatField(blank=True, default=0)
    received = models.FloatField(blank=True, default=0)
    sent = models.FloatField(blank=True, default=0)
    autoconsumption = models.FloatField(blank=True, default=0)
    consumption = models.FloatField(blank=True, default=0)

    date = models.DateField()

    def __str__(self):
        return f'{self.date.month}/{self.date.year}: {self.user.username}'
    

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')


    def save(self, *args, **kwargs):
        all_posts = Post.objects.filter(user=self.user)     
        self.date = datetime.date(self.date.year, self.date.month, 1)
        self.full_clean()

        #Setting previous month (and year if month was january)
        previous_post_date = self.date - relativedelta.relativedelta(months=1)
        next_post_date = self.date + relativedelta.relativedelta(months=1)

    
        try:
            previous_post = all_posts.get(date__month=previous_post_date.month, date__year=previous_post_date.year)
            calculate_month(self, previous_post)

        #If there is no post in previous month we cannot calculate this month stats
        except Post.DoesNotExist as e:
            print('There is no post in previous month')
        except Exception as e:
            print(e)

        try:
            next_post = all_posts.get(date__month=next_post_date.month, date__year=next_post_date.year)
            calculate_month(next_post, self)
            next_post.save()

        #If there is no post in previous month we cannot calculate this month stats
        except Post.DoesNotExist as e:
            print('There is no post in next month')
        except Exception as e:
            print(e)

        post = super(Post, self).save()
