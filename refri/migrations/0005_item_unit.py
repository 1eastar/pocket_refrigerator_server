# Generated by Django 3.0.6 on 2020-08-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refri', '0004_auto_20200705_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.CharField(default='개', max_length=1),
        ),
    ]
