# Generated by Django 4.0.2 on 2022-03-13 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateTimeField(verbose_name='date posted')),
                ('review_text', models.CharField(max_length=400)),
                ('rating_num', models.IntegerField(default=3)),
                ('redList_bool', models.BooleanField()),
                ('revieweeUserType', models.CharField(max_length=8)),
                ('reviewerName_text', models.CharField(max_length=40)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yardSite.customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yardSite.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('job_type', models.CharField(choices=[('LWN', 'Lawn Care'), ('LND', 'Landscaping'), ('GAR', 'Gardening/Plant Cultivation'), ('SNW', 'Snow Removal'), ('PET', 'Pet Care'), ('AUT', 'Automotive'), ('MOV', 'Moving Services'), ('CDN', 'Decoration')], max_length=3)),
                ('cash_reward', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('completed', models.BooleanField(default=False)),
                ('date_to_be_finished_by', models.DateField()),
                ('zip_code', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yardSite.customer')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yardSite.worker')),
            ],
        ),
    ]
