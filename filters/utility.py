import datetime

def convert_timestamp_to_datetime(created_time):
  return datetime.datetime.strptime(created_time,"%a %b %d %H:%M:%S +0000 %Y")
