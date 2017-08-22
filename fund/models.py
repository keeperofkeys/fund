import pandas as pd
from django.db import models

STRATEGY_OPTIONS = (
    ('multi', 'Multi Arbitrage'),
    ('fixed', 'Fixed Income'),
    ('long_short', 'Long Short Equity'),
    ('event', 'Event Driven'),
)

REGION_OPTIONS = (
    ('global', 'Global'),
    ('us', 'US'),
    ('asia', 'Asia'),
)


class Return(models.Model):
    percentage = models.DecimalField(decimal_places=2, max_digits=5)
    date = models.DateField()

    def __str__(self):
        return '%s%s on %s' % (self.percentage, '%', self.date.strftime('%d-%m-%Y'))

class Fund(models.Model):
    fund_id = models.CharField(max_length=20, unique=True, blank=False)
    name = models.CharField(max_length=255, blank=False)
    strategy = models.CharField(choices=STRATEGY_OPTIONS, max_length=10, blank=False)
    region_exposure = models.CharField(choices=REGION_OPTIONS, max_length=6)
    returns_series = models.ManyToManyField(Return, blank=True)

    def __str__(self):
        return self.name

    def get_time_series(self):
        time_data = self.returns_series.all()
        percentages = [td.percentage for td in time_data]
        dates = [td.date for td in time_data]
        return pd.Series(percentages, dates)

