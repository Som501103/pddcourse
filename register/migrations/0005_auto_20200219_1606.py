# Generated by Django 3.0.3 on 2020-02-19 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_auto_20200219_1529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list_emp',
            old_name='PK_List',
            new_name='PK_List_Emp',
        ),
    ]
