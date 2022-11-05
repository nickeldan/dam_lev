import typing


class Scorer:
    def __init__(self) -> None:
        self.champion = []
        self.score = -1

    def update(self, value: typing.List) -> None:
        length = len(value)
        if length < self.score or self.score < 0:
            self.champion = value
            self.score = length
