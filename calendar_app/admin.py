from django.contrib import admin
from .models import Month_Schedule

# Register your models here.


@admin.register(Month_Schedule)
class Month_Schedule_Admin(admin.ModelAdmin):
    list_display = ("cleared", 'schedule', 'created', 'updated_time')
