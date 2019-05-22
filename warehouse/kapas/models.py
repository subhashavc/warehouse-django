import binascii

import os
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.utils import timezone


class User(AbstractUser):
    user_type = ((1, 'Admin_user'), (2, 'Customer_Admin'), (3, 'Site_Manager'))
    UserType = models.PositiveIntegerField(default=1, choices=user_type)



def CreateGroup(sender, instance, *args, **kwargs):
    if instance._state.adding is True and len(Group.objects.filter(name=instance.get_UserType_display())) == 0:
        print("Group has been created successfully ")
        Group.objects.create(name=instance.get_UserType_display())


def Add_group_to_user(sender, instance, *args, **kwargs):
    try:
        if (instance.UserType == 1):
            User.objects.filter(username=instance.username).update(is_staff=True)
        g = Group.objects.filter(name=instance.get_UserType_display())
        print(g)
        print("Instance has been added inside the group")
        instance.groups.set(g)
    except:
        pass


post_save.connect(Add_group_to_user, sender=User)
pre_save.connect(CreateGroup, sender=User)


class Customer(models.Model):
    Name = models.CharField(max_length=20)
    Username = models.CharField(max_length=20, unique=True, verbose_name=u"Please Enter your Unique Username",
                                help_text=u"Please do not select white spaces", default='test123')
    Password = models.CharField(max_length=15, default="Pass123")
    Created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                   limit_choices_to={'UserType': 1, 'is_active': True})
    Total_Property = models.PositiveIntegerField(default=0)
    Email = models.EmailField(max_length=40, unique=True)
    Contact_no = models.CharField(max_length=10, null=True, blank=True)
    Address = models.CharField(max_length=200, blank=True, null=True)
    Contract_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.Name

    def __str__(self):
        return self.Name




def Remove_Customer_to_User(sender, instance, *args, **kwargs):
    User.objects.filter(username=instance.Username).update(is_active=False)


def Add_Customer_to_User(sender, instance, *args, **kwargs):
    if instance._state.adding is True:
        User.objects.create_user(username=instance.Username, email=instance.Email, UserType=2,
                                 password=instance.Password)
    else:
        pass


pre_save.connect(Add_Customer_to_User, sender=Customer)
post_delete.connect(Remove_Customer_to_User, sender=Customer)

# Site details table

class Site(models.Model):
    Site_Name = models.CharField(max_length=20, blank=True, null=True)
    Which_location = models.CharField(max_length=20, blank=True)
    Block_name = models.CharField(max_length=20, blank=True, null=True)
    Owner = models.ForeignKey(Customer, related_name='sites', on_delete=models.CASCADE, null=True, blank=True)
    site_type = ((0, "Normal_Block"),
                 (1, "Common_Block"),
                 (2, "warehouse"))
    Site_type = models.PositiveIntegerField(choices=site_type, default=0)
    Associated_floor = models.CharField(max_length=5, blank=True, null=True)
    powerStatus = ((0, 'OFF'), (1, 'ON'))
    Power_status = models.PositiveIntegerField(choices=powerStatus, default=1)
    Total_No_Of_Block = models.PositiveIntegerField(default=0)
    Total_No_Of_Aisle = models.PositiveIntegerField(default=0)
    Total_No_ofRow = models.PositiveIntegerField(default=0)
    Total_Lights = models.PositiveIntegerField(default=0)
    Cumulative_units = models.FloatField(default=0)
    saved_Units = models.FloatField(default=0)
    Shared_Cumulative = models.FloatField(default=0)
    Baseline_units = models.FloatField(default=0)
    Contact_Number = models.CharField(max_length=10, null=True, blank=True)
    Live_Date = models.DateTimeField(default=timezone.now)
    Unit_Rate_Utility = models.FloatField(default=0)
    Power_Backup_Rate_Utility = models.FloatField(default=0)
    Percentage_Saved_Energy = models.FloatField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)


    def __str__(self):
        return self.Site_Name

    # Daily Site Reading Tabel for graph
class DailySiteReading(models.Model):
    Which_Site_reading = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)
    SaveEnergy = models.FloatField(default=0, blank=True, null=True)
    Percentage_Saved = models.FloatField(default=0, blank=True, null=True)
    unit_consumption = models.FloatField(default=0, blank=True, null=True)
    Created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} reading on {}".format(self.Which_Site_reading, self.Created, self.unit_consumption)

class DailyMeterReadings(models.Model):
    which_Site_reading = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)
    unit_use = models.FloatField(default=0, blank=True, null=True)  # this is the reading in units
    Reading_of = ((0, 'Energy'), (1, 'Voltage'), (2, "Current"), (3, "Power"))
    reading_of = models.PositiveIntegerField(default=0, choices=Reading_of)
    unit_consumption = models.FloatField(default=0, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "{} reading on {}".format(self.which_Site_reading, self.created,self.unit_consumption)

    def __str__(self):
        return "{} reading on {}".format(self.which_Site_reading, self.created,self.unit_consumption)