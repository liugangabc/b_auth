# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('extra', models.TextField(null=True, blank=True)),
                ('type', models.CharField(max_length=255, choices=[('admin', 'Admin'), ('public', 'Public'), ('private', 'Private')])),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoleResource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('permission', models.BooleanField()),
                ('Resource', models.ForeignKey(to='b_auth.Resource')),
                ('role', models.ForeignKey(to='b_auth.Role')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('extra', models.TextField(null=True, blank=True)),
                ('role', models.ForeignKey(to='b_auth.Role')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
