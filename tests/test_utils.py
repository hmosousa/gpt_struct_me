from src.utils import string_overlap, is_sublist


def test_string_overlap_simple():
    src = "Edifício da Luanda Medical Center"
    tgt = "Luanda"
    assert string_overlap(src, tgt)


def test_string_overlap_missing():
    src = "Edifício da Luanda Medical Center"
    tgt = "not in source"
    assert not string_overlap(src, tgt)


def test_string_overlap_start():
    src = "Edifício da Luanda Medical Center"
    tgt = "not in string Edifício da Luanda"
    assert string_overlap(src, tgt)


def test_string_overlap_start2():
    src = "not in string Edifício da Luanda"
    tgt = "Edifício da Luanda Medical Center"
    assert string_overlap(src, tgt)


def test_string_overlap_end():
    src = "Edifício da Luanda Medical Center"
    tgt = "Center not in string"
    assert string_overlap(src, tgt)


def test_string_overlap_missing2():
    src = "Edifício da Luanda Medical Center"
    tgt = "Edifício Center"
    assert not string_overlap(src, tgt)


def test_string_overlap_missing3():
    src = "Edifício da Luanda Medical Center"
    tgt = ""
    assert not string_overlap(src, tgt)


def test_string_overlap_similar():
    src = "Psicologia"
    tgt = "Ps"
    assert not string_overlap(src, tgt)


def test_is_sublist():
    list1 = ["b", "c"]
    list2 = ["a", "b", "c", "d"]
    assert is_sublist(list1, list2)


def test_is_sublist_not_sequencial():
    list1 = ["a", "c"]
    list2 = ["a", "b", "c", "d"]
    assert not is_sublist(list1, list2)
