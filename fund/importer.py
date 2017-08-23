import math
import pandas as pd
from fund.models import Fund


def import_time_series(file_path):
    spreadsheet = pd.ExcelFile(file_path)
    sheets = spreadsheet.sheet_names

    # initialize Fund objects referenced in first sheet
    if 'Funds Details' in sheets:
        funds_info = spreadsheet.parse('Funds Details')
        for i in funds_info.T:  # transpose
            fi = funds_info.T[i]
            name = fi['Fund Name']
            style = fi['Strategy Style']
            region = fi['Region Exposure']
            f, flag = Fund.objects.get_or_create(name=name, strategy=style, region_exposure=region)
            f.save()
            if flag:
                print('created fund %s' % name)

    # populate
    if 'Time Series' in sheets:
        ts_data = spreadsheet.parse('Time Series')
        for fund_name in ts_data:
            fund_data = ts_data[fund_name]  # Series
            f = Fund.objects.get(name=fund_name)
            count = 0
            for item in fund_data.iteritems():
                date, percentage = item
                if not math.isnan(percentage):
                    f.add_return_item(date, percentage * 100)  # automatically saves
                    count += 1

            print('added %s items to %s' % (count, fund_name))
                


