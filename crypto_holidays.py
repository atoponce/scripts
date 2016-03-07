#!/usr/bin/python

# Crypto Holidays
#
# Inspired by https://twitter.com/hacks4pancakes/status/676143734346653700=
#
# Each month in the year gets a non-religious "crypto holiday" (static):
#   Found with SHA256($FULL_MONTH_NAME)
# Each year also gets a non-religious "crypto holiday" (dynamic):
#   Found with SHA256($4_DIGIT_YEAR)
#
# Other ideas for holidays:
#   * Hash-o-ween
#   * AES-giving
#   * Hackmas
#   * Satoshi Nakamoto Day
#   * Edward Snowden Day (hard-coded to June 5)
#   * Brute-Force Day
#
# Released to the public domain


import hashlib
import datetime

curr_year = datetime.datetime.now().year
months = {'January':   31, 'February': 28, 'March':    31, 'April':    30,
          'May':       31, 'June':     30, 'July':     31, 'August':   31,
          'September': 30, 'October':  31, 'November': 30, 'December': 31}

def crypto_day(month):
    day = int(hashlib.sha256(month).hexdigest(),16) % months[month]
    start_month = datetime.datetime.strptime(month,'%B')
    return (start_month + datetime.timedelta(days=day)).strftime('%m/%d')

def crypto_year():
    day = int(hashlib.sha256(str(curr_year)).hexdigest(),16) % 365
    start_day = datetime.datetime.strptime(str(curr_year), '%Y')
    return (start_day + datetime.timedelta(days=day)).strftime('%m/%d')


print('Crypto Holidays:')
print('  {0} year: {1}'.format(curr_year, crypto_year()))
print('  January: {0}'.format(crypto_day('January')))
print('  February: {0}'.format(crypto_day('February')))
print('  March: {0}'.format(crypto_day('March')))
print('  April: {0}'.format(crypto_day('April')))
print('  May: {0}'.format(crypto_day('May')))
print('  June: {0}'.format(crypto_day('June')))
print('  July: {0}'.format(crypto_day('July')))
print('  August: {0}'.format(crypto_day('August')))
print('  September: {0}'.format(crypto_day('September')))
print('  October: {0}'.format(crypto_day('October')))
print('  November: {0}'.format(crypto_day('November')))
print('  December: {0}'.format(crypto_day('December')))
