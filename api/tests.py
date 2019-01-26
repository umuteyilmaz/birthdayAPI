from datetime import timedelta, datetime, date
import json
from django.test import TestCase
from rest_framework.test import APITestCase
from . import models
from .views import BIRTDAY_DATE_FORMAT

class BirthdayTestCases(APITestCase):
    url = '/api/v1/{username}'

    def setUp(self):
        
        # create user with test_update username 
        # birtday with 5 days after today
        self.test_username = 'test_update'
        birthday = datetime.now() + timedelta(days=5)
        models.User.objects.create(
            username=self.test_username,
            birthday=birthday
        )
    
    def test_update_success(self):
        new_birthday = '2019-01-01'
        response = self.client.put(
            self.url.format(username=self.test_username),
            {
                'dateOfBirth': new_birthday
            },
            format='json'
        )

        # check respose status
        self.assertEqual(204, response.status_code)

        # check birthday is updated in db
        user = models.User.objects.get(username=self.test_username)
        new_birthday_date = datetime.strptime(new_birthday, BIRTDAY_DATE_FORMAT)
        self.assertEqual(user.birthday, new_birthday_date.date())

    def test_create_success(self):
        new_birthday = '2019-01-02'
        new_username = 'test_create'
        response = self.client.put(
            self.url.format(username=new_username),
            {
                'dateOfBirth': new_birthday
            },
            format='json'
        )

        # check respose status
        self.assertEqual(204, response.status_code)

        # check user is created correctly
        user = models.User.objects.get(username=new_username)
        new_birthday_date = datetime.strptime(new_birthday, BIRTDAY_DATE_FORMAT)
        self.assertEqual(user.birthday, new_birthday_date.date())
    
    def test_get_after_5_days(self):
        response = self.client.get(self.url.format(username=self.test_username))

        message = 'Hello, {username}! Your birthday is in {days} day{s}' \
            .format(username=self.test_username, days=5, s='s')
        
        # check message
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], message)

    def test_get_before_5_days(self):
        
        #create user with birthday is passed this year 
        new_username = 'test_before'
        new_birthday = date.today() - timedelta(days=5)
        models.User.objects.create(
            username=new_username,
            birthday=new_birthday
        )

        response = self.client.get(self.url.format(username=new_username))

        message = 'Hello, {username}! Your birthday is in {days} day{s}' \
            .format(username=new_username, days=360, s='s')
        
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], message)

    def test_get_before_today(self):
        
        #create user with birthday is today 
        new_username = 'test_today'
        new_birthday = date.today()
        models.User.objects.create(
            username=new_username,
            birthday=new_birthday
        )

        response = self.client.get(self.url.format(username=new_username))

        message = 'Hello, {username}! Happy birthday!' \
            .format(username=new_username)
        
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], message)