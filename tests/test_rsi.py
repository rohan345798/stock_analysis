import pytest
from rsi import calculate_rsi


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        ([25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25], 50.0),
        ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2], 100.0),
        ([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1.5], 50.0),
        ([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1.5], 0.0),
    ],
)
def test_rsi_all_same(test_input, expected_output):
    assert calculate_rsi(test_input) == expected_output
