from __future__ import unicode_literals

from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255, null=True, blank=True)


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255, null=True, blank=True)
    # passwd = models.CharField(max_length=255, null=True, blank=True)
    extra = models.TextField(null=True, blank=True)
    role = models.ForeignKey(Role)

    USERNAME_FIELD = 'name'


class Resource(models.Model):
    RESOURCE_TYPE = (
        ('admin', 'Admin'),
        ('public', 'Public'),
        ('private', 'Private'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    extra = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=RESOURCE_TYPE)


class RoleResource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role)
    Resource = models.ForeignKey(Resource)
    permission = models.BooleanField()
