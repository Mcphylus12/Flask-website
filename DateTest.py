import calendar


month = input('enter month index: ')
year = input('enter Year: ')
print(calendar.monthrange(int(year), int(month)))
