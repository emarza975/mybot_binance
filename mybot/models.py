from django.db import models
from django.utils import timezone

# Create your models here.
class Prices_db (models.Model):
    open_time = models.DateTimeField(default=timezone.now)
    symbol = models.CharField(max_length=13)
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField()
    close_time = models.DateTimeField(default=timezone.now)
    quote_asset_volume = models.FloatField()
    number_of_trades = models.FloatField()
    taker_buy_base_asset_volume = models.FloatField()
    taker_buy_quote_asset_volume = models.FloatField()
    ignore = models.IntegerField()

    class Meta:
        unique_together = [["open_time", "symbol"]]