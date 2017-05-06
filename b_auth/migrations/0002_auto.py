# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def user_init(apps, schema_editor):
    Role = apps.get_model("b_auth", "Role")
    admin_role = Role.objects.create(name='admin')
    private_role = Role.objects.create(name='private')
    User = apps.get_model("b_auth", "User")
    User.objects.create(name='admin', password='password', role=admin_role)
    User.objects.create(name='demo', password='password', role=private_role)


class Migration(migrations.Migration):
    dependencies = [
        ('b_auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(user_init),
    ]
