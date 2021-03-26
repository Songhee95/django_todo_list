from django.contrib import admin
from .models import List, Monthly


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ("todo_list", "updated_time", "created")


@admin.register(Monthly)
class MonthlyAdmin(admin.ModelAdmin):
    list_display = ("monthly_goal", "updated_time", "created")

# Register your models here.
