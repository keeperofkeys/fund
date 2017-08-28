import datetime
from django.shortcuts import render
from fund.models import Fund


def tabular_view(request):
    funds = list(Fund.objects.all())
    jun17 = datetime.date(2017, 6, 30)

    # if the june 2017 return were pivotal, I would store it in the db
    for fund in funds:
        cr = fund.get_cumulative_return()
        fund.return2017 = cr[jun17]

    funds.sort(key=lambda x: -x.return2017)

    return render(request, 'table.html', {
        'funds': funds
    })