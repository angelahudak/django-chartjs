import datetime


def str_to_datetime_date(datestr):
    """Convert a 'yyyy-mm-dd' string to a datetime.date object.
    """
    return datetime.datetime.strptime(datestr, "%Y-%m-%d").date()


def date_range(start_date, end_date, inclusive=True):
    """Generate a sequence of datetime.date objects.

    Arguments:
        start_date (datetime.date object or `yyyy-mm-dd'): Start date.
        end_date (datetime.date object or 'yyyy-mm-dd'): End date.
        inclusive (boolean): Whether or not to include `end_date` in the range.

    Yields:
        datetime.date object
    """
    if type(start_date) == str:
        start_date = str_to_datetime_date(start_date)
    if type(end_date) == str:
        end_date = str_to_datetime_date(end_date)
    number_of_days = int((end_date - start_date).days)
    if inclusive:
        number_of_days += 1
    for days in range(number_of_days):
        yield start_date + datetime.timedelta(days)


def value_or_null(start_date, end_date, queryset, date_attr, value_attr):
    """Generate a sequence of numbers or 'null' strings.

    This generator is used when you want to plot non-continuous datestamped data. For
    example, you might have data spanning three weeks, but you're missing data for the
    weekends, and you want to express that those data points are missing. If a queryset
    doesn't have a value for a particular date, then this generator yields a 'null'.

    Example:
        Suppose we have a model of automobiles and we're interested in plotting the
        number of trips to 7-11. (We're trying to estimate out Cheetos consumprion.)
        We can filter our automobiles model by make and model if we like, or not, and
        then dump that QuerySet into the `value_or_null` generator in order to produce
        either the number of trips to 7-11 that day, or a 'null' string, if no data is
        available for that date.

        >>> queryset = Automobiles.objects.filter(make="Subaru", model="Outback")
        >>> for value in util.value_or_null('2019-05-01', '2019-06-01', queryset, 'date', 'trips_to_711')
        [0, 1, 1, 'null', 3, 5, 8, 'null', ...]

    Arguments:
        start_date (datetime.date object or 'yyyy-mm-dd'): Start date.
        end_date: (datetime.date object or 'yyyy-mm-dd'): End date.
        queryset (QuerySet): Django queryset that we're interested in.
        date_attr (str): Name of date attribute of `queryset`.
        value_attr (str): Name of numerical value of interest of `queryset`.

    Yields:
        numeric value or 'null' string
    """
    NULL = "null"
    if type(start_date) == str:
        start_date = str_to_datetime_date(start_date)
    if type(end_date) == str:
        end_date = str_to_datetime_date(end_date)
    for new_date in date_range(start_date, end_date):
        query = {
            date_attr + "__year": new_date.year,
            date_attr + "__month": new_date.month,
            date_attr + "__day": new_date.day,
        }
        items = queryset.filter(**query)
        if items.count() == 1:
            yield vars(items.first())[value_attr]
        else:
            yield NULL
