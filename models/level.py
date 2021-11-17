class Level:
  id = 0
  name = "Test"
  mark = 0
  end = 0
  order = 0

  def __init__ (self, id = 0, name ="", mark=0, end=0, order=0):
    self.id = id
    self.name = name
    self.mark = mark
    self.end = end
    self.order = order

  # Chuyen du lieu cua object sang dictionary
  def asdict(self):
    return {
      "id" : self.id,
      "name": self.name,
      "mark": self.mark,
      "end": self.end,
      "order": self.order
    }