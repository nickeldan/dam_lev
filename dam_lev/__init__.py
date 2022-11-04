import dataclasses
import enum
import functools
import typing

VERSION = "0.1.0"


class Type(enum.Enum):
    INSERTION = "Insertion"
    DELETION = "Deletion"
    SUBSTITUTION = "Substitution"
    TRANSPOSITION = "Transposition"


T = typing.TypeVar("T")


@dataclasses.dataclass(slots=True, frozen=True)
class Mutation(typing.Generic[T]):
    type: Type
    at: int
    item: typing.Optional[T] = None

    def __repr__(self) -> str:
        word = f"{self.type.value}(at={self.at}"
        if self.item is not None:
            word += f", item={self.item}"
        return word + ")"


def get_changes(seq1: typing.Sequence[T], seq2: typing.Sequence[T]) -> typing.List[Mutation[T]]:
    @functools.lru_cache()
    def chain(i: int, j: int) -> typing.List[Mutation[T]]:
        if i < 0 and j < 0:
            return []

        possibles: typing.List[typing.List[Mutation[T]]] = []

        if i < 0 or j < 0:
            spots_differ = True
        else:
            spots_differ = seq1[i] != seq2[j]

        if spots_differ:
            if i >= 0:
                value = chain(i - 1, j) + [Mutation(type=Type.DELETION, at=i)]
                possibles.append(value)

            if j >= 0:
                value = chain(i, j - 1) + [Mutation(type=Type.INSERTION, at=i + 1, item=seq2[j])]
                possibles.append(value)

        if i >= 0 and j >= 0:
            prev_value = chain(i - 1, j - 1)
            if spots_differ:
                value = prev_value + [Mutation(type=Type.SUBSTITUTION, at=i, item=seq2[j])]
            else:
                value = list(prev_value)
            possibles.append(value)

            if i >= 1 and j >= 1 and seq1[i] == seq2[j - 1] and seq1[i - 1] == seq2[j]:
                value = chain(i - 2, j - 2) + [Mutation(type=Type.TRANSPOSITION, at=i - 1)]
                possibles.append(value)

        champion: typing.Optional[typing.List[Mutation[T]]] = None
        score = -1

        for value in possibles:
            length = len(value)
            if score == -1 or length < score:
                champion = value
                score = length

        return champion or []

    return chain(len(seq1) - 1, len(seq2) - 1)
