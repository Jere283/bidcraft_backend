# Generated by Django 5.0.6 on 2024-07-28 23:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KycStatus',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'kyc_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersKyc',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('front_id', models.CharField(blank=True, max_length=200, null=True)),
                ('back_id', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_picture', models.CharField(blank=True, max_length=200, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users_kyc',
                'managed': False,
            },
        ),
    ]
