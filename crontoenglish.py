# A simple module that converts a crontab line to English representation,
#
# Author: Kenny Chong
# Date: Nov 9th, 2013

import re

# test example
cron_line =  '1 0 31 * 5 echo "Hello Milk!"'

# list to represent day of the weeks.
DAY_OF_WEEK = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] 

# list to represent day of the months (1-12).
MONTH = ['null', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'
		,'September', 'October', 'November', 'December']
#
# Converts hour string from a 24-hour format into 12-hour
# format.
# 
# Input: A String that represents the hour in 24-hour format
# Output: A String that reprsents the hour in 12-hour format
#
# Throws error if:
# = The input is not a number
# - The input is empty
# - Not in 24-hour format (00-23)		
def convertToTwelveHour(hour):	
	hourVal = eval(hour)

	if hourVal == 0:
		return 12
	
	# checking if hourVal is between 13 - 23
	if hourVal > 12 and hourVal < 24:
		# subtract by 12 to get 12-hour format
		hourVal -= 12

	return hourVal

# Determine if hour is AM or PM. The hour is in 24-hour
# format.
#
# Input: The hour string in 24-hour format
# Output: String 'AM' or 'PM', depending on the hour
#
# Throws error if:
# - The input is an empty String
# - The input is not on 24-hour format
def checkTimeOfDay(hour):
	# input checking
	if hour == '*':
		return ''

	hourVal = eval(hour)
	
	# in 12-hour time, it would be between 12:00 AM to 11:00 AM
	if hourVal >= 0 and  hourVal < 12:
		return 'AM'

	return 'PM'

#
# Formats the minute interval. ex '1' minute will be '01' minute
#
def formatMinuteInterval(minute):
	if eval(minute) < 10:
		return '0{}'.format(minute)

	return minute
#
# Formats the day of the week interval, ex '0' will be Sunday, '1' will be Monday, etc.
#
def formatDayOfWeek(day_of_week):
	if day_of_week < 0 or day_of_week > 6:
		return 'error'

	return DAY_OF_WEEK[day_of_week]

#
# Formats month, ex '1' will be  January, '2' will be February, etc.
#
def formatMonth(month):
	if month < 1 or month > 12:
		return 'error'

	return MONTH[month]

#
# Determine whether the day_of_month should have a suffix 'th', 'rd', 'nd', or 'st', 
# ex: '1st', '22nd', '30th'
#
def deterDayOfMonthSuffix(day_of_month):
	if day_of_month < 1 or day_of_month > 31:
		return 'error'

	# return 'rd' for these days
	if day_of_month == 3 or day_of_month == 23:
		return 'rd'

	# return 'nd' for these days
	if day_of_month == 2 or day_of_month == 22:
		return 'nd'

	# return 'st' for these days
	if day_of_month == 1 or day_of_month == 21 or day_of_month == 31:
		return 'st'

	# return 'th' for any other days
	return 'th'

#
# Parses the minute and hour cron line and converts it into an English 
# represention.
# 
# Input: A single cron line represented as a String
# Output: An hour, minute String represent of the cron line 
#
# Throws error if:
# - The input is an empty String
# - The input is not a valid cron command
#
def parseTime(minute, hour):
	
	# we say something like 'runs x minutes past the hour'
	if hour == '*' and minute != '*':
		return minute + ' minutes past the hour'
	
	# we say something like 'runs at 11:00'
	if minute == '*' and hour != '*':
		return convertToTwelveHour(hour) + ":00"
	
	# we say something like 'runs every minute'
	if minute == '*' and hour == '*':
		return 'every minute'

	# say 'runs at h:m AM/PM'
	return 'at {}:{}'.format(convertToTwelveHour(hour), formatMinuteInterval(minute))
#
# Parses the date cron line and converts it into an English 
# represention.
# 
# Input: A single cron line represented as a String
# Output: A date String represent of the cron line 
#
# Throws error if:
# - The input is an empty String
# - The input is not a valid cron command
#
def parseDate(day_of_month, month, day_of_week):

	# examples of possible cron lines:
	# 0 1 * * * command means that it will run at 1:00 AM every day
	# * * 3 * * command means that it will run x mins/hours on '3rd of every month' of the year
	# * * * 4 * command means that it will run x mins/hours 'everyday' in 'April'
	# * * * * 5 command means that it will run x mins/hours every 'Friday' 
	# * * 4 2 * command means that it will run x mins/hours on 4th of Feburary'
	# * * 4 * 1 command means that it will run x mins/hours on '4th of every month' if that day of the week is 'Monday' 
	# * * * 3 2 command means that it will run x mins/hours every 'Tuesday' in 'March'
	# * * 1 7 3 command means that it will run x mins/hours on the '1st' of 'July' (July 1st) if that day of the week is 'Wednesday'
	
	# for day_of_week only
	if day_of_week != '*' and month == '*' and day_of_month == '*':
		return 'every ' + formatDayOfWeek(eval(day_of_week)) 

	# for day_of_month only
	if day_of_week == '*' and month == '*' and day_of_month != '*':
		return 'on ' + day_of_month + deterDayOfMonthSuffix(eval(day_of_month)) + ' of every month'

	# for month only
	if day_of_week == '*' and month != '*' and day_of_month == '*':
		return 'throughout ' + formatMonth(eval(month))

	# for day of the month and month, ex '4th of July'
	if day_of_week == '*' and day_of_month != '*' and month != '*':
		return 'on ' + day_of_month + deterDayOfMonthSuffix(eval(day_of_month)) + ' of ' + formatMonth(eval(month))
  
	# for day of the month and day of the week, ex '4th of every month if the 4th is a Monday'
	if day_of_week != '*' and day_of_month != '*' and month == '*':
		return ('on ' + day_of_month + deterDayOfMonthSuffix(eval(day_of_month)) + ' of every month if the '  
		        + day_of_month + deterDayOfMonthSuffix(eval(day_of_month)) + ' is a ' + formatDayOfWeek(eval(day_of_week)))
	
	# for day of the month and day of the week, ex 'every Tuesday in March'
	if day_of_week != '*' and day_of_month == '*' and month != '*':
		return 'every ' + formatDayOfWeek(eval(day_of_week)) + + ' in ' + formatMonth(eval(month))

	# for day of the month, day of the week, and month, ex '1st of July (July 1st) if the 1st is 'Wednesday'
	return ('on ' + formatMonth(eval(month)) + ' ' + day_of_month + deterDayOfMonthSuffix(eval(day_of_month)) + 
		' if the ' + day_of_month + deterDayOfMonthSuffix(eval(day_of_month)) + ' is a ' + formatDayOfWeek(eval(day_of_week)))

#	
# Converts cron to english.
# 
def convert(cron_line):
	# split cron_line String by whitespace
	split_line = re.split('\s', cron_line, 6)

	# retrieve minute
	cron_minute = split_line[0]

	# retrieve hour
	cron_hour = split_line[1]

	# retrieve day of the month
	cron_day_of_month = split_line[2]

	# retrieve month 
	cron_month = split_line[3]

	# retrieve day of the week (Mon,Tues, etc.)
	cron_day_of_week = split_line[4]
	
	print ('This command will run ' + parseTime(cron_minute, cron_hour) + ' ' + checkTimeOfDay(cron_hour) + ' ' + 
	      parseDate(cron_day_of_month, cron_month, cron_day_of_week)) 

convert(cron_line)
#print(formatMinuteInterval('11'))
#print parseDate('12', '5', '1')
