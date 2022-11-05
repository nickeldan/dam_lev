import dataclasses
import enum
import functools
import typing

from . import _util


class Type(enum.Enum):
    INSERTION = "Insertion"
    DELETION = "Deletion"
    SUBSTITUTION = "Substitution"
    TRANSPOSITION = "Transposition"


@dataclasses.dataclass(slots=True, frozen=True)
class Mutation:
    type: Type
    at: int
    at2: int = -1

    def __repr__(self) -> str:
        word = f"{self.type.value}(at={self.at}"
        if self.at2 >= 0:
            word += f"at2={self.at2}"
        return word + ")"


def get_changes(
    seq1: typing.Sequence, seq2: typing.Sequence, key: typing.Optional[typing.Callable] = None
) -> typing.List[Mutation]:
    if key is None:
        key = lambda x: x

    @functools.lru_cache()
    def chain(i: int, j: int) -> typing.List[Mutation]:
        if i < 0 and j < 0:
            return []

        scorer = _util.Scorer()

        item1 = key(seq1[i])
        item2 = key(seq2[j])

        spots_differ = i < 0 or j < 0 or item1 != item2

        if spots_differ:
            if i >= 0:
                scorer.update(hain(i - 1, j) + [Mutation(type=Type.DELETION, at=i)])

            if j >= 0:
                scorer.update(chain(i, j - 1) + [Mutation(type=Type.INSERTION, at=i + 1, at2=j)])

        if i >= 0 and j >= 0:
            prev_value = chain(i - 1, j - 1)
            if spots_differ:
                scorer.update(prev_value + [Mutation(type=Type.SUBSTITUTION, at=i, at2=j)])
            else:
                scorer.update(list(prev_value))

            if i >= 1 and j >= 1 and item1 == key(seq2[j - 1]) and key(seq1[i - 1]) == item2:
                scorer.update(chain(i - 2, j - 2) + [Mutation(type=Type.TRANSPOSITION, at=i - 1)])

        return scorer.champion

    return chain(len(seq1) - 1, len(seq2) - 1)
