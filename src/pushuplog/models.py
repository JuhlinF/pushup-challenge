from django.db import models
from django.conf import settings
from django.utils import timezone


class PushupLogEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    sets = models.SmallIntegerField(default=1, blank=True)
    repetitions = models.SmallIntegerField()
    when = models.DateTimeField(default=timezone.now, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PushupSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal = models.IntegerField(default=50_000)
