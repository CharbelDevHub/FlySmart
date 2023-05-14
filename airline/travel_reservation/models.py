from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    receive_promotions = models.BooleanField(
        default=False
    )
    birthdate = models.DateField(
        null=True,blank=True
    )


