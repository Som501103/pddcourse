# Generated by Django 3.0.3 on 2021-03-16 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0024_course_d_course_detail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course_d',
            old_name='End_Time',
            new_name='End_Register',
        ),
        migrations.RenameField(
            model_name='course_d',
            old_name='Start_Time',
            new_name='Open_Register',
        ),
    ]