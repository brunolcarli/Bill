# Generated by Django 2.1.10 on 2019-07-24 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='abp.League'),
        ),
    ]
