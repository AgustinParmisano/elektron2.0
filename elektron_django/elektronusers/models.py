# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator

class ElektronUser(User):
    username_validator = ASCIIUsernameValidator()

    class Meta:
        proxy = True  # If no new field is added.
