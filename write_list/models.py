from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class List(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)
    todo_list = models.CharField(max_length=5000)
    created = models.DateTimeField()
    updated_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user}, {self.cleared}, {self.todo_list}, {self.updated_time}, {self.created}"

    # class Meta:
    #     verbose_name_plural = 'Lists'


class Monthly(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    cleared = models.BooleanField(default=False)
    monthly_goal = models.CharField(max_length=5000)
    created = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user}, {self.cleared}, {self.monthly_goal}, {self.updated_time}, {self.created}"
