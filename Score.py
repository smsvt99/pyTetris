class Score(object):
    def __init__(self, tuple):
        self.id = tuple[0]
        self.name = tuple[1]
        self.score = tuple[2]

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score
        }