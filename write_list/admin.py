from django.contrib import admin
from .models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ("todo_list", "updated_time", "created")


# Register your models here.
