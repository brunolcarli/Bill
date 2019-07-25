# Generated by Django 2.1.10 on 2019-07-24 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abp', '0004_auto_20190724_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='league_season',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='abp.Season'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='league',
            name='league_trainers',
            field=models.ManyToManyField(to='abp.Trainer'),
        ),
    ]