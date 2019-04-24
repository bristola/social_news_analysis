import pytest
from data_collector import *
from twitter_collector import *


d1 = Twitter_Collector("","","","")


@pytest.mark.parametrize(
    "data,expected",
    [
        ([{"author":"author1","text":"Some text"}],[{"author":"author1","text":"Some text"}]),
        ([{"author":"author1","text":"Some text"},{"author":"author1","text":"Another text"}],[{"author":"author1","text":"Some text"}])
    ]
)
def test_filter_authors(data, expected):
    out_data = d1.filter_authors(data)
    assert out_data == expected
