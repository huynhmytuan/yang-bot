
class User:
  user_id = 0
  name = "xinchao"
  learning_time = 0
  day_learning = 0
  week_learning = 0
  month_learning = 0
  semester_learning = 0
  current_level = -1
  highest_rank = -1
  join_time = 0
  
  def __init__(self, user_id = 0, name = "", learning_time = 0, day_learning = 0, week_learning = 0, month_learning = 0, semester_learning = 0, current_level = -1, highest_rank = -1 , join_time = 0):
      self.user_id = user_id
      self.name = name
      self.learning_time = learning_time
      self.day_learning = day_learning
      self.week_learning = week_learning
      self.month_learning = month_learning
      self.semester_learning = semester_learning
      self.current_level = current_level
      self.highest_rank = highest_rank
      self.join_time = join_time

  # Chuyen du lieu cua object sang dictionary
  def asdict(self):
    return {
      'user_id' : self.user_id,
      'name' : self.name,
      'learning_time' : self.learning_time,
      'day_learning' : self.day_learning,
      'week_learning' : self.week_learning,
      'month_learning' : self.month_learning,
      'semester_learning' : self.semester_learning,
      'current_level' : self.current_level,
      'highest_rank' : self.highest_rank,
      'join_time' : self.join_time
    }

  def getTime(self, time_type: str):
    if time_type == "month_learning":
      return self.month_learning
    elif time_type == "week_learning":
      return self.week_learning
    elif time_type == "day_learning":
      return self.day_learning
    elif time_type == "semester_learning":
      return self.semester_learning
    elif time_type == "learning_time":
      return self.learning_time


