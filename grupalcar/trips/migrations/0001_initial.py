# Generated by Django 2.2.5 on 2019-09-17 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pools', '0003_invitation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time of the object creation', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time of the object modification', verbose_name='modified at')),
                ('available_seats', models.PositiveSmallIntegerField(default=1)),
                ('comments', models.TextField(blank=True)),
                ('departure_location', models.CharField(max_length=255)),
                ('departure_date', models.DateTimeField()),
                ('arrival_location', models.CharField(max_length=255)),
                ('arrival_date', models.DateTimeField()),
                ('rating', models.FloatField(null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Used for disabling the trip or marking it as finished.', verbose_name='active status')),
                ('offered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('offered_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pools.Pool')),
                ('passengers', models.ManyToManyField(related_name='passengers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
