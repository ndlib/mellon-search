#getValidDate.py 2/7/19 sm
''' This module tries to clean up messy dates, returning a valid date string (not time) or nothing at all. '''

import datetime

def _get_valid_date(originalDate):
  validDate = ""
  validDate = _get_date_from_YYYY_MM_DD(originalDate) # example 2019-02-07
  if validDate == "":
    validDate = _get_date_from_YYYY_MM(originalDate) # example 2019-02
  if validDate == "":
    validDate = _get_date_from_YYYY(originalDate) # example 2019
  if validDate == "":
    validDate = _get_date_from_YYYYMMDD(originalDate) # example 20190207
  if validDate == "":
    validDate = _get_date_from_YYYYMM(originalDate) #  example 201902
  if validDate == "":
    validDate = _get_date_from_MMsDDsYYYY(originalDate) # example 12/31/2018
  if validDate == "":
    validDate = _get_date_from_YYYY_(originalDate) # example 2019 - 2019
  if type(validDate) == datetime.datetime:
    return ('{:%Y-%m-%d}'.format(validDate))
  else:
    return("")

def getValidISODate(passedDateString):
  dateString = ""
  validDate = datetime.datetime.strptime(_get_valid_date(passedDateString), '%Y-%m-%d')
  if type(validDate) == datetime.datetime:
    dateString = '{:%Y-%m-%d}'.format(validDate)
  return(dateString)

def getValidYYYYMMDDDate(passedDateString):
  dateString = ""
  try:
    validDate = datetime.datetime.strptime(_get_valid_date(passedDateString), '%Y-%m-%d')
    if type(validDate) == datetime.datetime:
      dateString = "{:%Y%m%d}".format(validDate)
  except ValueError:
    pass
  return(dateString)

def _get_date_from_YYYY_MM_DD(originalDate):
  validDate = ""
  try:
    validDate = datetime.datetime.strptime(originalDate, '%Y-%m-%d')
  except ValueError:
    pass
  return(validDate)

def _get_date_from_YYYYMMDD(originalDate):
  validDate = ""
  try:
    validDate = datetime.datetime.strptime(originalDate, '%Y%m%d')
  except ValueError:
    pass
  return(validDate)

def _get_date_from_YYYYMM(originalDate):
  validDate = ""
  try:
    validDate = datetime.datetime.strptime(originalDate, '%Y%m')
  except ValueError:
    pass
  return(validDate)

def _get_date_from_YYYY_MM(originalDate):
  validDate = ""
  try:
    validDate = datetime.datetime.strptime(originalDate, '%Y-%m')
  except ValueError:
    pass
  return(validDate)

def _get_date_from_YYYY(originalDate):
  validDate = ""
  try:
    validDate = datetime.datetime.strptime(originalDate, '%Y')
  except ValueError:
    pass
  return(validDate)

def _get_date_from_YYYY_(originalDate): #Trying to capture year from "2019- 2019"
  validDate = ""
  try:
    if len(originalDate) >= 4: #Must have at least YYYY as start of string
      validDate = datetime.datetime.strptime(originalDate[:4], '%Y')
  except ValueError:
    pass
  return(validDate)

def _get_date_from_MMsDDsYYYY(originalDate): #Trying to capture year from "2/7/2019"
  validDate = ""
  try:
    validDate = datetime.datetime.strptime(originalDate, '%m/%d/%Y')
  except ValueError:
    pass
  return(validDate)

# python3 -c 'from getValidDate import *; test()'
def test():
  try:
    assert(_get_valid_date('2019-02-07') == '2019-02-07')
    assert(_get_valid_date('2019-02') == '2019-02-01')
    assert(_get_valid_date('2019') == '2019-01-01')
    assert(_get_valid_date('20190207') == '2019-02-07')
    assert(_get_valid_date('201902') == '2019-02-01')
    assert(_get_valid_date('2019 - 2019') == '2019-01-01')
    assert(getValidISODate('2019-02-07') == '2019-02-07')
    assert(getValidYYYYMMDDDate('2019-02-07') == '20190207')
    assert(getValidYYYYMMDDDate('18910101') == '18910101')
    assert(_get_valid_date('2/7/2019') == '2019-02-07')
    assert(_get_valid_date('0 - 0') == '')
    print('All tests successfully passed.')

  except:
    raise
