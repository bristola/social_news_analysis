import pytest
from analysis import *

a = Analyzer()

@pytest.mark.parametrize(
    "word,lemma",
    [
        ("test", True),
        ("word", True),
        ("computer", True),
        ("twitter", True),
        ("news", True),
        ("https://github.com/", False),
        ("https://twitter.com/", False),
        ("http://t.co", False),
        ("and", False),
        ("are", False),
        ("of", False),
        ("on", False),
        ("where", False),
        ("most", False),
        ("more", False),
        ("should", False),
        ("them", False)
    ]
)
def test_is_valid_lemma(word, lemma):
    out_lemma = a.is_valid_lemma(word)
    assert out_lemma == lemma


# def test_prepare_data():
#     assert True
#
#
# def test_get_sentiment():
#     assert True
#
#
# def test_get_emoticons_value():
#     assert True
#
#
# def test_get_mood():
#     assert True
