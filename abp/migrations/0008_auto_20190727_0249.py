# Generated by Django 2.1.10 on 2019-07-27 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abp', '0007_auto_20190725_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_key', models.CharField(max_length=50)),
                ('score_key', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='leader',
            name='nickname',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='reference',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='leaguescore',
            name='reference',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='tournamentscore',
            name='reference',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='nickname',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AddField(
            model_name='event',
            name='trainer_reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abp.Trainer'),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('trainer_reference', 'event_key')},
        ),
    ]