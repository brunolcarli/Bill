# Generated by Django 2.1.10 on 2020-02-02 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abp', '0014_trainer_exp'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='discord_id',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='name',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
    ]
