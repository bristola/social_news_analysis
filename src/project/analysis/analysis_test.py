import pytest
from analysis import *

a = Analyzer()

@pytest.mark.parametrize(
    "word,valid",
    [
        ("test", False),
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
def test_is_valid_lemma(word, valid):
    out_lemma = a.is_valid_lemma(word)
    assert out_lemma == valid


@pytest.mark.parametrize(
    "data,result",
    [
        ("This is a test", ["test"]),
        ("This is a test. This is another one that is good.", ["test.", "another one good."]),
        ("What a sentance! Is it good?", ["sentance!", "good?"])
    ]
)
def test_prepare_data(data, result):
    out_data = a.prepare_data(data)
    assert out_data == result


@pytest.mark.parametrize(
    "sentances,greater,value",
    [
        (["good sentance!"], True, 0),
        (["bad sentance!"], False, 0),
        (["appalling hateful disgusting words.","awfully bad terms"], False, -.5),
        (["helpful and kind people","nice sweet things"], True, .5),
        (["the worst ever so disorganized everything fall apart"], False, -.25),
        (["Cute fluffy and love."], True, .8)
    ]
)
def test_get_sentiment(sentances, greater, value):
    out_value = a.get_sentiment(sentances)
    if greater:
        assert out_value > value
    else:
        assert out_value < value


@pytest.mark.parametrize(
    "line,emoticons",
    [
        ("There are no emotes here.", []),
        ("This is some smiley face 😊", ["😊"]),
        ("A few emotes here😭😴. As well as here 😎.", ["😭","😴","😎"])
    ]
)
def test_get_emoticons_value(line, emoticons):
    out_emotes = a.get_emoticons_value(line)
    assert out_emotes == emoticons


@pytest.mark.parametrize(
    "sentances,moods",
    [
        (["This is a merry sentance that I enjoy."], {"happiness": 2,"anxiety": 0,"sadness": 0,"affection": 0,"aggression": 0,"expressive": 0,"glory": 0}),
        (["I'm very afraid of this test."], {"happiness": 0,"anxiety": 1,"sadness": 0,"affection": 0,"aggression": 0,"expressive": 0,"glory": 0}),
        (["This is very sad to me!"], {"happiness": 0,"anxiety": 0,"sadness": 1,"affection": 0,"aggression": 0,"expressive": 0,"glory": 0}),
        (["I cherish these moments"], {"happiness": 0,"anxiety": 0,"sadness": 0,"affection": 1,"aggression": 0,"expressive": 0,"glory": 0}),
        (["They were aggressive!"], {"happiness": 0,"anxiety": 0,"sadness": 0,"affection": 0,"aggression": 1,"expressive": 0,"glory": 0}),
        (["The song was sang well."], {"happiness": 0,"anxiety": 0,"sadness": 0,"affection": 0,"aggression": 0,"expressive": 1,"glory": 0}),
        (["The crowd applaud the performers."], {"happiness": 0,"anxiety": 0,"sadness": 0,"affection": 0,"aggression": 0,"expressive": 0,"glory": 1})
    ]
)
def test_get_mood(sentances, moods):
    out_moods = a.get_mood(sentances)
    assert out_moods == moods
