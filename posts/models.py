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

    #Calculated fields
    #Energy used just after production
    #produced - sent
    autoconsumption = models.FloatField(blank=True, default=0, editable=False)

    #Percentage of autoconsumption from production
    #(produced - sent) / produced
    autoconsumption_percentage = models.FloatField(blank=True, default=0, editable=False)

    #Energy used this month
    #produced - sent + received
    consumption = models.FloatField(blank=True, default=0, editable=False)

    #Average energy used per day in month
    #(produce - sent + received) / count of days in month
    consumption_average = models.FloatField(blank=True, default=0, editable=False)

    #Deferred energy
    #sum of (sent * 0.8 or 0.7(Based on rules user is on)) from each month year back
    energy_surplus = models.FloatField(blank=True, default=0, editable=False)


    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')


    def __str__(self):
        return f'{self.date.month}/{self.date.year}: {self.user.username}'
    

    def clean(self):
        #Checking if all necessary values are filled
        if self.produced is None and self.produced_all is None or self.received is None and self.received_all is None or self.sent is None and self.sent_all is None:
            raise ValidationError('You need to fill required fields')
        try:
            if Post.objects.get(date__month=self.date.month, date__year=self.date.year, user=self.user).id != self.id:
                raise ValidationError('Post on this date already exists')
        except Post.DoesNotExist:
            pass


    def save(self, *args, **kwargs):
        #Setting variables
        energy_sent_back = 0.7 if self.user.userconfig.pv_power > 10 else 0.8
        user_posts = Post.objects.filter(user=self.user)

        #Setting post date to first day of the month to avoid multiple post in one month (easy validation)
        self.date = datetime.date(self.date.year, self.date.month, 1)

        #Saving next month post creates a chain that we control with this date
        #Last post that we will be saving cannot be past one year ahead from starter post
        last_date = kwargs.get('last_date')
        if last_date is None:
            last_date = self.date + relativedelta.relativedelta(years=+1)

        #Getting dates month back and month forward to calculate
        previous_post_date = self.date - relativedelta.relativedelta(months=1)
        next_post_date = self.date + relativedelta.relativedelta(months=1)

        try:
            previous_post = user_posts.get(date__month=previous_post_date.month, date__year=previous_post_date.year)

            #Gettting posts from one year back to calculate energy surplus
            #Current post isn't included because it could be edited thus it might differ
            date_year_back = self.date + relativedelta.relativedelta(years=-1, months=+1)
            year_back_posts = user_posts.filter(date__range=[date_year_back, previous_post_date])
            
            #Calculating this month stats
            calculate_month(self, previous_post)
            self.energy_surplus = sum([(post.sent * energy_sent_back) - post.received for post in year_back_posts])

            #Manualy adding current post data
            self.energy_surplus += (self.sent * energy_sent_back) - self.received

        #If there is no post in previous month we cannot calculate this month stats
        except Post.DoesNotExist as e:
            if self.sent_all is None:
                self.sent_all = self.sent
            else:
                self.sent = self.sent_all
            if self.received_all is None:
                self.received_all = self.received
            else:
                self.received = self.received_all
            if self.produced_all is None:
                self.produced_all = self.produced
            else:
                self.produced = self.produced_all
            print('There is no post in previous month')
            pass
        except Exception as e:
            print(e)

        super(Post, self).save()

        try:
            next_post = user_posts.get(date__month=next_post_date.month, date__year=next_post_date.year)

            #Check if last_date is later than next post date avoiding goingh through all posts
            if last_date > next_post.date:
                calculate_month(next_post, self)
                next_post.save(last_date=last_date)

        #If there is no post in next month we cannot calculate stats for it
        except Post.DoesNotExist as e:
            print('There is no post in next month')
            pass
        except Exception as e:
            print(e)

