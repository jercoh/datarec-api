# Product popularity ranking algorithm
# Inspired by Reddit's hot algorithm

from datetime import datetime, timedelta
from math import log

epoch = datetime(1970, 1, 1)
# tau = 17735274
tau = 1728000

def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def hot(sales, date):
    """The hot formula."""
    s = sales if (isinstance(sales, int)) else int(sales)
    order = log(max(abs(s), 1), 10)
    seconds = epoch_seconds(date) - 1134028003
    return round(order + seconds / tau, 7)