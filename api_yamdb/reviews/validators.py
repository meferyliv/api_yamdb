import datetime

from django.core.validators import MaxValueValidator


def current_year_validator():
    current_year = datetime.date.today().year
    return MaxValueValidator(current_year())
