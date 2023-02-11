from django.db import models

# Create your models here.


class Whatsapp(models.Model):
    name = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    language = models.CharField(max_length=15, default='English')
    alertStatus = models.CharField(max_length=15, default='ON', editable=False)
    temperatureAlert = models.IntegerField(default=1)
    machineVoltage = models.IntegerField(default=12)
    lastmessage = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Whatsapp User"
        verbose_name = "Whatsapp User"


class SmsUser(models.Model):
    name = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    language = models.CharField(max_length=15, default='English')
    alertStatus = models.CharField(max_length=15, default='ON', editable=False)
    temperatureAlert = models.IntegerField(default=1)
    machineVoltage = models.IntegerField(default=12)
    lastmessage = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "SMS User"
        verbose_name = "SMS User"