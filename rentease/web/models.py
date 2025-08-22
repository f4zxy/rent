from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('RENTER', 'Renter'),
        ('LENDER', 'Lender'),
        ('ADMIN', 'Admin'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='RENTER'
    )

    can_manage_users = models.BooleanField(default= False)
    can_manage_content = models.BooleanField(default=False)
