import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (5, 5, 10),
    (10, -3, 7),
])
def test_add(a, b, expected):
    assert a + b == expected