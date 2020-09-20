from django.db import models
from django.utils import timezone


class Customer(models.Model):
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    postal_code = models.CharField(max_length=6)
    creation_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.creation_time = timezone.now()
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        if self.email:
            return "[Email] %s" % self.email
        if self.phone:
            return "[Phone] %s" % self.phone
        return "Unknown"
