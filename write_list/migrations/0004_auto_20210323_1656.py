# Generated by Django 3.1.7 on 2021-03-23 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('write_list', '0003_auto_20210323_1650'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Month',
        ),
        migrations.AlterField(
            model_name='list',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]