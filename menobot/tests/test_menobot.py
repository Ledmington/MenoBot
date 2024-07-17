import pytest
from menobot.menobot.card import Card
from menobot.menobot.user import User
import random


def test_user_negative_id():
    with pytest.raises(ValueError):
        User(-1)


def test_new_user_follows_no_cards():
    u = User(123)
    assert u.get_interesting_cards() == []


def test_price_cannot_be_negative():
    c = Card("test", " https://test.com")
    with pytest.raises(ValueError):
        c.update_price(-1)


def test_new_card_has_no_price():
    c = Card("test", "ttps://test.com")
    assert c.get_prices() == []


def test_new_price():
    c = Card("test", "https://test.com")
    x = random.uniform(0.0, 1.0)
    c.update_price(x)
    assert len(c.get_prices()) == 1
    assert c.get_prices()[0][0] == x
