# Generated by Django 3.1.7 on 2021-04-01 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('write_list', '0009_auto_20210331_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]