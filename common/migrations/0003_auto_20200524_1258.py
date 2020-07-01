# Generated by Django 3.0.6 on 2020-05-24 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refri', '0002_refrigerator_memo_num'),
        ('common', '0002_auto_20200524_0424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='mainhonor',
        ),
        migrations.AddField(
            model_name='userdata',
            name='main_honor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Honor'),
        ),
        migrations.AlterField(
            model_name='barcode',
            name='basicitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='refri.BasicItem'),
        ),
        migrations.AlterField(
            model_name='barcode',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='refri.Item'),
        ),
    ]
