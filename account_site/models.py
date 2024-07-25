import uuid

from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)

    objects = models.Manager()

    def __str__(self):
        return f'Profile of {self.user.name}'


class ActiveTokenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=6, unique=False)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = models.Manager()
    active_objects = ActiveTokenManager()
