# constants for certain time integer values
NOON = 1200
ONE_PM = 1300
TEN_AM = 1000

# function to convert between integer time value used for database and 12 hour time used in the UI
def twelveHourTime(number):
   time = ""
   timePeriod = "AM"

   # check if time is AM or PM
   if number >= NOON:
      timePeriod = "PM"

      # convert from 24 hour to 12 hour time
      if number >= ONE_PM:
         number -= NOON

   # construct the 12 hour time string
   temp = str(number)
   if number < TEN_AM:
      time = temp[0] + ':' + temp[1] + temp[2] + timePeriod
   else:
      time = temp[0] + temp[1] + ':' + temp[2] + temp[3] + timePeriod

   return time

# function to compute number of hours between two integer time values
def hoursBetween(end_time, start_time):
   # use integer division to get the number of hours
   hours = (end_time - start_time) / 100
   # use floating point division to get decimal value
   minutes = (end_time - start_time) / 100.0

   # remove the hours from minutes
   if hours > 0:
       minutes = minutes % hours

   # change 30 minutes to be represented as .5 hours
   if minutes != 0.0:
      minutes = 0.5

   return hours + minutes