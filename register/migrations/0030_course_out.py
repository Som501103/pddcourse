# Generated by Django 3.0.7 on 2022-04-19 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0029_subject_sub_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course_out',
            fields=[
                ('Course_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Course_number', models.FloatField(default=0.0)),
                ('Course_name', models.CharField(max_length=150, null=True)),
                ('Description', models.TextField(default='เนื้อหาที่จะเรียน', null=True)),
                ('Course_location', models.CharField(blank=True, max_length=100)),
                ('Course_user', models.CharField(blank=True, max_length=100)),
                ('Course_user_position', models.CharField(blank=True, max_length=100)),
                ('Course_generation', models.IntegerField(default=1, null=True)),
                ('Course_startdate', models.DateField(null=True)),
                ('Course_enddate', models.DateField(null=True)),
                ('Course_status', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]