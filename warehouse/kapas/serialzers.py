import logging

import time
from django.contrib.auth import authenticate
from django.core import exceptions
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.utils import json

from warehouse.kapas.models import User, Customer, Site, DailySiteReading

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'UserType')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key','user')


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username = data.get("username"," ")
        password = data.get("password", " ")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data["user"] = user

            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
           msg = "Must provide username and password both."
           raise exceptions.ValidationError(msg)
        return data

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'Name','Username', 'Total_Property', 'Email', 'Contact_no', 'Address')

    def meraTesting(self):
        testUsername = Customer.objects.get()



class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'
        depth = 2


class DailySiteReadingSerializer(serializers.ModelSerializer):
    Which_Site_reading = serializers.ReadOnlyField(source='Which_Site_reading.Site_Name')
    Created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = DailySiteReading
        fields = ('Which_Site_reading', 'id', 'SaveEnergy', 'Percentage_Saved', 'unit_consumption', 'Created')


