from datetime import datetime, date
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from . import models

BIRTDAY_DATE_FORMAT = '%Y-%m-%d'

class UserViewSet(viewsets.ViewSet):
    """
        viewset for creating, updating and getting user birthdays
    """
    def put(self, request, username):
        if 'dateOfBirth' not in request.data :
            return Response({'dateOfBirth': 'add birthday to request'},
                        status=status.HTTP_400_BAD_REQUEST)

        # get strig datetime
        birthday_str = request.data['dateOfBirth']

        # parse birtday
        try:
            birthday = datetime.strptime(birthday_str, BIRTDAY_DATE_FORMAT)
        
        except ValueError:

            # return 400 if birtdat format is wrong
            return Response(
                {
                    'dateOfBirth': 'Wrong birtday format valit format: YYYY-MM-DD'
                }, 
                status=status.HTTP_400_BAD_REQUEST)
        
        # check birtday is before now
        if birthday>datetime.now():
            return Response(
                {
                    'dateOfBirth': 'Birtday must be before now'
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # create user if not exists or get user
        user, created = models.User.objects.get_or_create(
            username=username,
            defaults={'birthday': birthday}
        )

        # if it exist update birtday
        if not created:
            user.birthday = birthday
            user.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

   
    def get(self, request, username):
        try:
            user = models.User.objects.get(username=username)
        
        except models.User.DoesNotExist:
            
            # user with this username doesnot exists
            return Response(
                {
                    'detail': 'user with this Username doesnot exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # find how many days before
        birthday = user.birthday
        today = date.today()
        this_year_birtday = birthday.replace(year=today.year)
        time_diff = today - this_year_birtday

        # check birtday is passed this year
        if today<this_year_birtday:
            time_diff_days = -1*time_diff.days
        else:
            time_diff_days = 365-time_diff.days

        # create message
        if time_diff_days==365:
            message = 'Hello, {username}! Happy birthday!'.format(username=user.username)
        else:
            message = 'Hello, {username}! Your birthday is in {days} day{s}' \
                .format(
                    username=user.username,
                    days=time_diff_days,
                    s='s' if time_diff_days>1 else ''
                )
        
        return Response({'message': message})
    