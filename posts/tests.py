from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from datetime import date

class PostTest(TestCase):
    def testPostModel(self):
        user = User.objects.create(username='adam', password='adam123')
        
        date1 = date(2022, 1, 1)
        post1 = Post.objects.create(user=user, produced_all=454, received_all=345, sent_all=345, date=date1)
        self.assertEqual(post1.sent, 345)

        date2 = date(2022, 2, 1)
        post2 = Post.objects.create(user=user, produced=111, received_all=388, sent_all=395, date=date2)
        self.assertEqual(post2.consumption, 104)
        self.assertEqual(post2.balance, -57.6)

        date3 = date(2022, 3, 1)
        post3 = Post.objects.create(user=user, produced=123, received_all=600, sent=324, date=date3)
        self.assertEqual(post3.autoconsumption_percentage, -1.63)

        date5 = date(2022, 5, 1)
        post5 = Post.objects.create(user=user, produced=432, received=123, sent=233, date=date5)

        date4 = date(2022, 4, 1)
        post4 = Post.objects.create(user=user, produced=234, received=242, sent=123, date=date4)
        self.assertEqual(post4.energy_surplus, -168.4)
        post5 = Post.objects.get(date=date5)
        self.assertEqual(post5.consumption_average, 10.39)

        date6 = date(2022, 6, 1)
        post6 = Post.objects.create(user=user, produced=678, received=167, sent=270, date=date6)
        self.assertEqual(post6.energy_surplus, -56)

        date7 = date(2022, 7, 1)
        post7 = Post.objects.create(user=user, produced=1024, received=122, sent=333, date=date7)
        self.assertEqual(post7.consumption_average, 26.23)
        self.assertEqual(post7.energy_surplus, 144.4)