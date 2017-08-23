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


class Fund(models.Model):
    #fund_id = models.CharField(max_length=20, unique=True, blank=False)
    name = models.CharField(max_length=255, blank=False, unique=True)
    strategy = models.CharField(choices=STRATEGY_OPTIONS, max_length=10, blank=False)
    region_exposure = models.CharField(choices=REGION_OPTIONS, max_length=6)
    #returns_series = models.ManyToManyField(ReturnItem, blank=True)

    def __str__(self):
        return self.name

    def get_time_series(self):
        time_data = self.returnitem_set.all()
        percentages = [td.percentage for td in time_data]
        dates = [td.date for td in time_data]
        pds = pd.Series(percentages, dates)
        return pds

    def add_return_item(self, date, percentage):
        self.returnitem_set.create(
            date=date,
            percentage=percentage
        )


class ReturnItem(models.Model):
    percentage = models.DecimalField(decimal_places=2, max_digits=5)
    date = models.DateField()
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)

    def __str__(self):
        return '%s%s on %s' % (self.percentage, '%', self.date.strftime('%d-%m-%Y'))

