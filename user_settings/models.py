from django.db import models
from django.contrib.auth.models import User


class UserConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pv_power = models.FloatField(("Plant Efficiency (kW)"), default=0)
    settlement_month = models.IntegerField(("Month of settlement (1-12)"), default=1)

    BILLING = 'billing'
    METERING = 'metering'
    RULES_CHOICES = [
        (BILLING, 'Net-Billing (nowe zasady)'),
        (METERING, 'Net-Metering (stare zasady)'),
    ]
    rules = models.CharField(("PV billing rules"), choices=RULES_CHOICES, default=METERING, max_length=50)


    def __str__(self):
        return f"Config: {self.user.username}"
    