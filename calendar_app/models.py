from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Month_Schedule(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)
    schedule = models.CharField(max_length=5000)
    created = models.DateTimeField()
    updated_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user}, {self.cleared}, {self.schedule}, {self.created}, {self.updated_time}"
