import dam_lev


def test_diff_empty() -> None:
    diffs = dam_lev.get_changes("", "")
    assert isinstance(diffs, list)
    assert not diffs


def test_transposition() -> None:
    assert dam_lev.get_changes("ab", "ba") == [dam_lev.Transposition(at=0)]


def test_substitution() -> None:
    assert dam_lev.get_changes("a", "b") == [dam_lev.Substitution(at=0, at2=0)]


def test_insertion() -> None:
    assert dam_lev.get_changes("a", "ab") == [dam_lev.Insertion(at=1, at2=1)]


def test_deletion() -> None:
    assert dam_lev.get_changes("a", "") == [dam_lev.Deletion(at=0)]


def test_transposition_then_substitution() -> None:
    assert dam_lev.get_changes("abc", "bad") == [
        dam_lev.Transposition(at=0),
        dam_lev.Substitution(at=2, at2=2),
    ]


def test_transposition_then_insertion() -> None:
    assert dam_lev.get_changes("ab", "bac") == [dam_lev.Transposition(at=0), dam_lev.Insertion(at=2, at2=2)]


def test_transposition_then_deletion() -> None:
    assert dam_lev.get_changes("abc", "ba") == [dam_lev.Transposition(at=0), dam_lev.Deletion(at=2)]


def test_substitution_then_transposition() -> None:
    assert dam_lev.get_changes("abc", "xcb") == [
        dam_lev.Substitution(at=0, at2=0),
        dam_lev.Transposition(at=1),
    ]


def test_substitution_then_insertion() -> None:
    assert dam_lev.get_changes("a", "bc") == [
        dam_lev.Substitution(at=0, at2=0),
        dam_lev.Insertion(at=1, at2=1),
    ]


def test_substitution_then_deletion() -> None:
    assert dam_lev.get_changes("ab", "c") == [dam_lev.Substitution(at=0, at2=0), dam_lev.Deletion(at=1)]


def test_insertion_then_transposition() -> None:
    assert dam_lev.get_changes("ab", "cba") == [dam_lev.Insertion(at=0, at2=0), dam_lev.Transposition(at=0)]


def test_insertion_then_substitution() -> None:
    assert dam_lev.get_changes("abc", "xabd") == [
        dam_lev.Insertion(at=0, at2=0),
        dam_lev.Substitution(at=2, at2=3),
    ]


def test_insertion_then_deletion() -> None:
    assert dam_lev.get_changes("abc", "xab") == [dam_lev.Insertion(at=0, at2=0), dam_lev.Deletion(at=2)]


def test_deletion_then_transposition() -> None:
    assert dam_lev.get_changes("abc", "cb") == [dam_lev.Deletion(at=0), dam_lev.Transposition(at=1)]


def test_deletion_then_substitution() -> None:
    assert dam_lev.get_changes("abcd", "bce") == [dam_lev.Deletion(at=0), dam_lev.Substitution(at=3, at2=2)]


def test_deletion_then_insertion() -> None:
    assert dam_lev.get_changes("abc", "bcd") == [dam_lev.Deletion(at=0), dam_lev.Insertion(at=3, at2=2)]


def test_with_key() -> None:
    assert dam_lev.get_changes("aBc", "AbC", key=str.upper) == []


def test_different_types() -> None:
    assert dam_lev.get_changes("abc", ["a", "b"]) == [dam_lev.Deletion(at=2)]


def test_nonhashable_elements() -> None:
    assert dam_lev.get_changes([[1, 2], [3, 4]], [[1], [3, 4]]) == [dam_lev.Substitution(at=0, at2=0)]
