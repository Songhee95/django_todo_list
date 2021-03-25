from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class List(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    todo_list = models.CharField(max_length=5000)
    created = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f" {self.todo_list}, {self.updated_time}, {self.created}"

    # class Meta:
    #     verbose_name_plural = 'Lists'
