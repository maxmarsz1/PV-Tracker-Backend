from django.test import TestCase
from .models import UserConfig
from django.contrib.auth.models import User
from posts.models import Post
from datetime import date

class UserConfigTest(TestCase):
    def testUserStartingValues(self):
        user = User.objects.create(username='adam', password='adam123')
        userconfig = user.userconfig
        userconfig.rules = 'billing'
        userconfig.energy_buy_price = 0.7
        userconfig.energy_sell_price = 0.3
        userconfig.produced_start = 100
        userconfig.received_start = 200
        userconfig.sent_start = 300

        date1 = date(2022, 1, 1)
        post1 = Post.objects.create(user=user, produced_all=554, received_all=345, sent_all=345, date=date1)
        self.assertEqual(post1.sent, 45)
        self.assertEqual(post1.balance, -88)

        date2 = date(2022, 2, 1)
        post2 = Post.objects.create(user=user, produced=111, received_all=388, sent_all=395, date=date2)
        self.assertEqual(post2.produced_all, 665)
        self.assertEqual(post2.balance, -103.1)

        date3 = date(2022, 3, 1)
        post3 = Post.objects.create(user=user, produced=123, received_all=600, sent=324, date=date3)
        self.assertEqual(post3.received, 212)
        self.assertEqual(post3.balance, -154.3)
