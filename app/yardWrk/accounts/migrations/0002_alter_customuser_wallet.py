# Generated by Django 4.0.2 on 2022-04-05 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='wallet',
            field=models.IntegerField(default=0),
        ),
    ]
