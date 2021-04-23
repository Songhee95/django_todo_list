from django.contrib import admin
from .models import List, Monthly, Joint


@admin.register(Joint)
class JointAdmin(admin.ModelAdmin):
    list_display = ('user', 'joint_id')


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('user', "todo_list", "updated_time", "created")


@admin.register(Monthly)
class MonthlyAdmin(admin.ModelAdmin):
    list_display = ('user', "monthly_goal", "updated_time", "created")

# Register your models here.
