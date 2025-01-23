from django.db import models
from django.conf import settings
from django.utils import timezone


class PushupLogEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    repetitions = models.SmallIntegerField()
    when = models.DateTimeField(default=timezone.now, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "pushup log entries"


class PushupSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal = models.IntegerField(default=50_000)
