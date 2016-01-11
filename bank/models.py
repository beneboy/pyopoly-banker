from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Player(models.Model):
    name = models.TextField()
    balance = models.DecimalField(max_digits=6, decimal_places=2)
