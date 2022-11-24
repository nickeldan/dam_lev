import dataclasses
import functools
import typing


@dataclasses.dataclass
class Mutation:
    at: int
    at2: int = -1

    def __repr__(self) -> str:
        word = f"{self.__class__.__name__}(at={self.at}"
        if self.at2 >= 0:
            word += f", at2={self.at2}"
        return word + ")"


class Transposition(Mutation):
    pass


class Substitution(Mutation):
    pass


class Insertion(Mutation):
    pass


class Deletion(Mutation):
    pass


class Scorer:
    def __init__(self) -> None:
        self.champion: typing.List[Mutation] = []
        self.score = -1

    def update(self, value: typing.List[Mutation]) -> None:
        length = len(value)
        if length < self.score or self.score < 0:
            self.champion = value
            self.score = length


def get_changes(
    seq1: typing.Sequence, seq2: typing.Sequence, key: typing.Optional[typing.Callable] = None
) -> typing.List[Mutation]:
    if key is None:
        key = lambda x: x
    else:
        key = functools.lru_cache(key)

    @functools.lru_cache(maxsize=None)
    def chain(i: int, j: int) -> typing.List[Mutation]:
        if i < 0 and j < 0:
            return []

        scorer = Scorer()

        assert key is not None  # mypy issue 2608
        spots_differ = i < 0 or j < 0 or key(seq1[i]) != key(seq2[j])

        if i >= 1 and j >= 1 and key(seq1[i]) == key(seq2[j - 1]) and key(seq1[i - 1]) == key(seq2[j]):
            scorer.update(chain(i - 2, j - 2) + [Transposition(at=i - 1)])

        if spots_differ:
            if i >= 0:
                scorer.update(chain(i - 1, j) + [Deletion(at=i)])

            if j >= 0:
                scorer.update(chain(i, j - 1) + [Insertion(at=i + 1, at2=j)])

        if i >= 0 and j >= 0:
            prev_value = chain(i - 1, j - 1)
            if spots_differ:
                scorer.update(prev_value + [Substitution(at=i, at2=j)])
            else:
                scorer.update(list(prev_value))

        return scorer.champion

    return chain(len(seq1) - 1, len(seq2) - 1)
