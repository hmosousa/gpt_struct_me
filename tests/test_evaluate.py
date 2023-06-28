from src.evaluate import (
    macro_averaged_f1_score,
    entity_f1_score,
    exact_match
)


def test_entity_f1_score():

    annt = 'integrar'
    pred = 'Bens passam a integrar património'

    tp, fp, fn = entity_f1_score(pred, annt)
    assert tp == 1
    assert fp == 4
    assert fn == 0


def test_entity_f1_score_punctiation():

    annt = 'integrar'
    pred = 'Bens passam a integrar, património'

    tp, fp, fn = entity_f1_score(pred, annt)
    assert tp == 1
    assert fp == 4
    assert fn == 0


def test_macro_averaged_f1_score():

    annt = set(['integrar', 'passam'])
    pred = set(['Fundos públicos', 'Bens passam a integrar património'])

    f1 = macro_averaged_f1_score(pred, annt)

    assert round(f1, 3) == round(2/7, 3)


def test_macro_averaged_f1_score_prefect():

    annt = set(['Fundos públicos', 'Bens passam a integrar património'])
    pred = set(['Fundos públicos', 'Bens passam a integrar património'])

    f1 = macro_averaged_f1_score(pred, annt)

    assert f1 == 1


def test_macro_averaged_f1_score_punctuation():

    annt = set(['integrar', 'passam'])
    pred = set(['Fundos públicos', 'Bens ,passam! a integrar, património'])

    f1 = macro_averaged_f1_score(pred, annt)

    assert round(f1, 3) == round(2/7, 3)


def test_exact_match():

    annt = set(['integrar', 'passam', 'loja'])
    pred = set(['Bens', 'passam', 'a', 'integrar', 'património'])

    tp, fp, fn = exact_match(pred, annt)

    assert tp == 2
    assert fp == 3
    assert fn == 1
