import datetime
import calendar
import pywhatkit
def add_days_to_month():
    start_day = datetime.date.today()
    current_month_duration = calendar.monthrange(start_day.year, start_day.month)
    return current_month_duration[1]

def setMembershipData(durationOfMembership, monthsList, daysList, startMont, startYear, counter1, counter2):
    iterator = 0
    if durationOfMembership == 'three-months':
        iterator = 3
    elif durationOfMembership == 'half-year':
        iterator = 6
    elif durationOfMembership == 'one-year':
        iterator = 12
    for i in range(iterator):
        monthsList.append(counter1 + startMont)
        if counter1 + startMont == 12:
            counter1 = 0
            startMont = datetime.date(startYear + 1, 1, 1).month
        else:
            counter1 = counter1 + 1
    for i in monthsList:
        if counter2 > i:
            daysList.append(calendar.monthrange(startYear + 1, i)[1])
            counter2 = i
        elif counter2 <= i:
            daysList.append(calendar.monthrange(startYear, i)[1])
            counter2 = counter2 + 1
    return monthsList, daysList


def add_days_for_three_months(durationOfMembership):
    listOfMonths = []
    daysOfThreeMonths = []
    start_month = datetime.date.today().month
    start_year = datetime.date.today().year
    counterForMonth = 0
    control_counter = start_month
    setMembershipData(durationOfMembership, listOfMonths, daysOfThreeMonths, start_month, start_year, counterForMonth, control_counter)
    return sum(daysOfThreeMonths)
days = datetime.date.today() - datetime.date(2022, 8, 2)
print(type(days.days))





