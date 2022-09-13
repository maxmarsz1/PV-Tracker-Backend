from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .utils import calculate_month

import datetime
from dateutil import relativedelta


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #Fields to fill
    #Energy stats for this month
    produced_all = models.FloatField(blank=True)
    received_all = models.FloatField(blank=True)
    sent_all = models.FloatField(blank=True)

    #Energy stats from meter
    produced = models.FloatField(blank=True)
    received = models.FloatField(blank=True)
    sent = models.FloatField(blank=True)
    date = models.DateField()

    # Calculated fields
    # Energy used just after production
    # produced - sent
    autoconsumption = models.FloatField(blank=True, default=0, editable=False)

    # Percentage of autoconsumption from production
    # autoconsumption / produced
    autoconsumption_percentage = models.FloatField(blank=True, default=0, editable=False)

    # Energy used this month
    # produced - sent + received
    consumption = models.FloatField(blank=True, default=0, editable=False)

    # Average energy used per day in month
    # consumption / count of days in month
    consumption_average = models.FloatField(blank=True, default=0, editable=False)

    # Deferred energy
    # sum of (sent * 0.8 or 0.7(Based on rules user is on)) from each month year back
    energy_surplus = models.FloatField(blank=True, default=0, editable=False)

    # Deferred energy in cash
    # energy_surplus * user.userconfig.energy_buy_price
    energy_surplus_cash = models.FloatField(blank=True, default=0, editable=False)


    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')


    def __str__(self):
        return f'{self.date.month}/{self.date.year}: {self.user.username}'
    

    def clean(self):
        # Checking if all necessary values are filled
        if self.produced is None and self.produced_all is None or self.received is None and self.received_all is None or self.sent is None and self.sent_all is None:
            raise ValidationError('You need to fill required fields')
        try:
            if Post.objects.get(date__month=self.date.month, date__year=self.date.year, user=self.user).id != self.id:
                raise ValidationError('Post on this date already exists')
        except Post.DoesNotExist:
            pass


    def save(self, *args, **kwargs):
        # Setting variables
        user_posts = Post.objects.filter(user=self.user)

        # Setting post date to first day of the month to avoid multiple post in one month (easy validation)
        self.date = datetime.date(self.date.year, self.date.month, 1)

        # Saving next month post creates a chain that we control with this date
        # Last post that we will be saving cannot be past one year ahead from starter post
        last_date = kwargs.get('last_date')
       
        # Runs if this is base post - post that is created or edited
        # We're later updating next post with new data, so when we're saving next post we don't want
        # this to calculate same month again
        if last_date is None:
            # Calculating this month stats
            calculate_month(self, user_posts, Post)
            last_date = self.date + relativedelta.relativedelta(years=+1)

        super(Post, self).save()

        try:
            next_post_date = self.date + relativedelta.relativedelta(months=1)
            next_post = user_posts.get(date__month=next_post_date.month, date__year=next_post_date.year)

            # Check if last_date is later than next post date avoiding goingh through all posts
            if last_date > next_post.date:
                calculate_month(next_post, user_posts, Post)
                next_post.save(last_date=last_date)

        # If there is no post in next month we cannot calculate stats for it
        except Post.DoesNotExist:
            pass
        except Exception as e:
            print(e)

