# Generated by Django 2.0.2 on 2018-02-27 22:59

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('schedule', '0004_auto_20180227_1758'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Class',
            new_name='Course',
        ),
        migrations.RenameModel(
            old_name='ScheduleClass',
            new_name='ScheduleCourse',
        ),
    ]