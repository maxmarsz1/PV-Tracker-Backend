from django.db import models
from django.contrib.auth.models import User


class UserConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pv_power = models.FloatField(("Plant Efficiency (kW)"), default=0)
    produced_start = models.FloatField(('Produced starting value (inverter)'), default=0)
    received_start = models.FloatField(('Received starting value (1.8.0)'), default=0)
    sent_start = models.FloatField(('Sent starting value (2.8.0)'), default=0)

    PERIODS = (
        (1, '1 month'),
        (2, '2 months'),
        (6, '6 months'),
        (12, '12 months'),
    )
    settlement_month = models.IntegerField(("First month of settlement (1-12)"), default=6)
    settlement_period = models.IntegerField(choices=PERIODS, default=6)

    BILLING = 'billing'
    METERING = 'metering'
    RULES_CHOICES = [
        (BILLING, 'Net-Billing (nowe zasady)'),
        (METERING, 'Net-Metering (stare zasady)'),
    ]
    rules = models.CharField(("PV billing rules"), choices=RULES_CHOICES, default=METERING, max_length=50)

    # These two can differ only when rules are set to BILLING
    energy_buy_price = models.FloatField(("Buying price for 1kWh (PLN)"), default=0.8)
    energy_sell_price = models.FloatField(("Selling price for 1kWh (PLN)"), default=0.8)

    def __str__(self):
        return f"Config: {self.user.username}"


    def save(self, *args, **kwargs):
        if self.rules == self.METERING:
            self.energy_sell_price = self.energy_buy_price
        super(UserConfig, self).save()
    