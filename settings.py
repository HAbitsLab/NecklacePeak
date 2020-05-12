import pytz
from datetime import date

settings = {}

settings['TIMEZONE'] = pytz.timezone('America/Chicago')
# settings['ROOT_DIR'] = '/Volumes/Shibo/Periodic/' # PUT YOUR ABSOLUTE PATH OF ROOT FOLDER
settings['ROOT_DIR'] = 'C://Github//Peakpackage//test' # change this to your test directory, it is in this folder.

# 'START_DATE' contains all the participants' start day.
settings['START_DATE'] = {\
    'P103': date(2017, 6, 19),\
    'P105': date(2017, 6, 23),\
    'P107': date(2017, 7, 12),\
    'P108': date(2017, 8, 3),\
    'P110': date(2017, 8, 4),\
    'P114': date(2017, 8, 9),\
    'P116': date(2017, 8, 11),\
    'P118': date(2017, 8, 18),\
    'P120': date(2017, 8, 23),\
    'P121': date(2017, 8, 24),\
    'P201': date(2018, 12, 21),\
    'P202': date(2018, 12, 22),\
    'TEST': date(2018, 12, 27),\
    '203-2': date(2019, 1, 12),\
    '205': date(2019, 1, 20),\
    '206': date(2019, 1, 24),\
    '207': date(2019, 1, 28),\
    '208': date(2019, 1, 30),\
    '209': date(2019, 2, 3),\
    '210': date(2019, 2, 7),\
    '211': date(2019, 2, 7),\
    '212': date(2019, 2, 9),\
}

# 'DISCRETE_DATES' contains only those subjects with interrupted day(s) during the study
settings['DISCRETE_DATES'] = {\
    # '211': [date(2019, 2, 7), date(2019, 2, 8)]\
    '209': [date(2019, 2, 3), date(2019,2,5)]\
}

settings['CALENDAR_DAY_AMEND_HOURS'] = 5
