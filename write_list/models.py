from django.db import models

# Create your models here.


class List(models.Model):
    todo_list = models.CharField(max_length=5000)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.todo_list)

    # class Meta:
    #     verbose_name_plural = 'Lists'
