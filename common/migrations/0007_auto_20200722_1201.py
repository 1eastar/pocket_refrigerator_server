# Generated by Django 3.0.6 on 2020-07-22 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20200705_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='birth',
            field=models.CharField(default='0000', max_length=4),
        ),
        migrations.AddField(
            model_name='userdata',
            name='gender',
            field=models.IntegerField(default=0),
        ),
    ]
