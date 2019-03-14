# get_valid_date.py 2/7/19 sm
""" Returning a valid date string (not time) or nothing at all. """

import datetime


def _get_valid_date(original_date):
    """ Validates date and returns string in ISO format or empty string """
    valid_date = ""
    valid_date = _get_date_from_yyyy_mm_dd(original_date)  # example 2019-02-07
    if valid_date == "":
        valid_date = _get_date_from_yyyy_mm(original_date)  # example 2019-02
    if valid_date == "":
        valid_date = _get_date_from_yyyy(original_date)  # example 2019
    if valid_date == "":
        valid_date = _get_date_from_yyyymmdd(original_date)  # example 20190207
    if valid_date == "":
        valid_date = _get_date_from_yyyymm(original_date)  # example 201902
    if valid_date == "":
        valid_date = _get_date_from_mm_s_dd_s_yyyy(original_date)
        # example 12/31/2018
    if valid_date == "":
        valid_date = _get_date_from_yyyy_(original_date)  # example 2019 - 2019
    if isinstance(valid_date, datetime.datetime):
        return '{:%Y-%m-%d}'.format(valid_date)
    return ""


def get_valid_iso_date(passed_date_string):
    """ Public method to return ISO date string """
    date_string = ""
    try:
        valid_date = datetime.datetime.strptime(_get_valid_date(
            passed_date_string), '%Y-%m-%d')
    except ValueError:
        pass  # return no string if not valid date
    else:
        if isinstance(valid_date, datetime.datetime):
            date_string = '{:%Y-%m-%d}'.format(valid_date)
    return date_string


def get_valid_yyyymmdd_date(passed_date_string):
    """ Return date string in YYYYMMDD format or empty string """
    date_string = ""
    try:
        valid_date = datetime.datetime.strptime(_get_valid_date(
            passed_date_string), '%Y-%m-%d')
        if isinstance(valid_date, datetime.datetime):
            date_string = "{:%Y%m%d}".format(valid_date)
    except ValueError:
        pass
    return date_string


def _get_date_from_yyyy_mm_dd(original_date):
    """ If date is in ISO format, return date """
    valid_date = ""
    try:
        valid_date = datetime.datetime.strptime(original_date, '%Y-%m-%d')
    except ValueError:
        pass
    return valid_date


def _get_date_from_yyyymmdd(original_date):
    """ if date is in YYYYMMDD format, return date """
    valid_date = ""
    try:
        valid_date = datetime.datetime.strptime(original_date, '%Y%m%d')
    except ValueError:
        pass
    return valid_date


def _get_date_from_yyyymm(original_date):
    """ if date is in YYYYMM format, return date """
    valid_date = ""
    try:
        valid_date = datetime.datetime.strptime(original_date, '%Y%m')
    except ValueError:
        pass
    return valid_date


def _get_date_from_yyyy_mm(original_date):
    """ if date is in YYYY-MM format, return date """
    valid_date = ""
    try:
        valid_date = datetime.datetime.strptime(original_date, '%Y-%m')
    except ValueError:
        pass
    return valid_date


def _get_date_from_yyyy(original_date):
    """ if date is in YYYY format, return date """
    valid_date = ""
    try:
        valid_date = datetime.datetime.strptime(original_date, '%Y')
    except ValueError:
        pass
    return valid_date


def _get_date_from_yyyy_(original_date):
    # Trying to capture year from "2019 - 2019"
    """ if date starts with YYYY, return date as YYYY-01-01 """
    valid_date = ""
    try:
        if len(original_date) >= 4:  # Must have at least YYYY
            valid_date = datetime.datetime.strptime(original_date[:4], '%Y')
    except ValueError:
        pass
    return valid_date


def _get_date_from_mm_s_dd_s_yyyy(original_date):
    # Trying to capture year from "2/7/2019"
    """ if date is in MM/DD/YYYY format, return date """
    valid_date = ""
    try:
        valid_date = datetime.datetime.strptime(original_date, '%m/%d/%Y')
    except ValueError:
        pass
    return valid_date
