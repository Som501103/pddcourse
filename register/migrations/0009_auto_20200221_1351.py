# Generated by Django 3.0.3 on 2020-02-21 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0008_auto_20200219_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_emp',
            name='Dep',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='list_emp',
            name='Fullname',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]
