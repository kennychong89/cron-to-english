# A simple module that converts a chrontab line to English representation,
#
# Author: Kenny Chong
# Date: Nov 9th, 2013

import re

# test example
chron_line =  '11 * 3 * 5 * echo "Hello Milk!"'

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
	hourVal = eval(hour)

	# in 12-hour time, it would be between 12:00 AM to 11:00 AM
	if hourVal >= 0 and  hourVal < 12:
		return 'AM'

	return 'PM'

#
# Parses the chron line and converts it into an English 
# represention.
# 
# Input: A single chron line represented as a String
# Output: A String represent of the chron line 
#
# Throws error if:
# - The input is an empty String
# - The input is not a valid chron command
#
def parse(chron_line):
	# split chron_line String by whitespace
	split_line = re.split('\s', chron_line, 6)

	# retrieve minute
	chron_minute = split_line[0]

	# retrieve hour
	chron_hour = split_line[1]

	if chron_hour != '*':
		# convert 24-hour format into 12-hour formt
		twelveHourFor = convertToTwelveHour(chron_hour)
	
		# determine if it is AM or PM	
		timeOfDay = checkTimeOfDay(chron_hour)

		time = "{}:{} {}".format(twelveHourFor, chron_minute, timeOfDay)
	
		# display results (test)
		#time = twelveHourFor + ':' + chron_minute + ' ' + timeOfDay

		result = 'The command "' + split_line[6] + '" will run at ' + time

		print result
	else:
		# we say something like 'command runs x minutes past every hour'
		time = chron_minute + ' minutes'
		
		# ignore the leading '0' in the minute
		if chron_minute[0] == '0':	
			time = chron_minute[1] + ' minute'

		print 'The command "' + split_line[6] + '" will run ' + time + ' past every hour'

parse(chron_line)
