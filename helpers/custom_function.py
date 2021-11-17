def time_readable(time):
  if time < 0.017:
    return '--'
  elif time < 1:
    time_in_min = round(time * 60)
    time_str = str(time_in_min) + 'p'
    return time_str
  else:
    hours = int(time)
    mins = int((time - hours)*60)
    if mins > 0:
      return str(str(hours)+"h"+str(mins)+"p")
    else: 
      return str(str(hours)+"h")
