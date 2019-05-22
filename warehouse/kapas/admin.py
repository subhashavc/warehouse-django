from django.contrib import admin
#from warehouse.kapas.models import User, Customer, Site, DailySiteReading, DailyMeterReadings
from .models import *

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['usename', 'email', 'UserType']


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Contact_no', 'Total_Property', 'Email','Address']
    class Meta:
        model = Customer

class DailyMeterReadingsadmin(admin.ModelAdmin):
    list_display =['unit_use','which_Site_reading','unit_consumption','created']



admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Site)
admin.site.register(DailySiteReading)
admin.site.register(DailyMeterReadings, DailyMeterReadingsadmin)
