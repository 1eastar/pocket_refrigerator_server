# Generated by Django 3.0.6 on 2020-08-08 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20200705_0618'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0011_auto_20200808_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='report_object_id',
        ),
        migrations.AlterField(
            model_name='report',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='recipe.Comment'),
        ),
        migrations.AlterField(
            model_name='report',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='recipe.Recipe'),
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]