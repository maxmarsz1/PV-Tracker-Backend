from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from datetime import date

class PostTest(TestCase):
    def testPostModel(self):
        user = User.objects.create(username='adam', password='adam123')
        
        date1 = date(2022, 1, 1)
        post1 = Post.objects.create(user=user, produced_all=233, received_all=230, sent_all=120, date=date1)
        self.assertEqual(post1.sent, 120)

        date2 = date(2022, 2, 1)
        post2 = Post.objects.create(user=user, produced=412, received_all=429, sent_all=430, date=date2)
        self.assertEqual(post2.consumption, 301)

        date3 = date(2022, 3, 1)
        post3 = Post.objects.create(user=user, produced=354, received_all=530, sent=125, date=date3)
        self.assertEqual(post3.autoconsumption_percentage, 0.65)

        date4 = date(2022, 4, 1)
        post4 = Post.objects.create(user=user, produced=670, received=84, sent=432, date=date4)
        self.assertEqual(post4.energy_surplus, 175.6)