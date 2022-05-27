"""Tests for statistics functions within the Model layer."""

import numpy as np
import numpy.testing as npt
import pytest

@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0]),
        ([[1, 2], [3, 4], [5, 6]], [3, 4]),
    ]
)
def test_daily_mean(test, expected):
    """Test that mean function works for array of zeros and positive integers"""
    from inflammation.models import daily_mean
    npt.assert_array_equal(daily_mean(np.array(test)), np.array(expected))


@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0]),
        ([[-1, -2], [-3, -4], [-5, -6]], [-1, -2]),
        ([[1, -2], [-3, 4], [5, -6]], [5, 4])
    ]
)
def test_daily_max(test, expected):
    """Test that max function works for an array of zeros and negative integers and mixed integers."""
    from inflammation.models import daily_max

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_max(np.array(test)), np.array(expected))


@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0]),
        ([[-1, -2], [-3, -4], [-5, -6]], [-5, -6]),
        ([[1, -2], [-3, 4], [5, -6]], [-3, -6])
    ]
)
def test_daily_min(test, expected):
    """Test that min function works for an array of zeros and negative integers and mixed integers."""
    from inflammation.models import daily_min

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_min(np.array(test)), np.array(expected))


def test_daily_min_string():
    """Test for TypeError when passing strings"""
    from inflammation.models import daily_min

    with pytest.raises(TypeError):
        error_expected = daily_min([['Hello', 'there'], ['General', 'Kenobi']])


@pytest.mark.parametrize(
    "test, expected, expect_raises",
    [
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], None),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]], None),
        ([[float('nan'), 1, 1], [1, 1, 1], [1, 1, 1]], [[0, 1, 1], [1, 1, 1], [1, 1, 1]], None),
        ([[1, 2, 3], [4, 5, float('nan')], [7, 8, 9]],[[0.33, 0.67, 1], [0.8, 1, 0], [0.78, 0.89, 1]], None),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]], None),
        ([[-1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]], ValueError),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], [0.11, 0.22, 0.33, 0.44, 0.56, 0.67, 0.78, 0.89, 1], TypeError),
        ("hello", None, TypeError),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]], None),
    ]
)
def test_patient_normalise(test, expected, expect_raises):
    """Test normalisation works for arrays of one and positive integers.
    Assumption that accuracy of 2d.p. is sufficient."""
    from inflammation.models import patient_normalise
    if isinstance(test, list):
        test = np.array(test)
    if expect_raises is not None:
        with pytest.raises(expect_raises):
            npt.assert_almost_equal(patient_normalise(test), np.array(expected), decimal=2)
    else:
        npt.assert_almost_equal(patient_normalise(test), np.array(expected), decimal=2)


@pytest.mark.parametrize(
    "test, expected, expect_raises",
    [
        ([[[1, 2, 3], [4, 5, 6], [7, 8, 9]], ["Gregg", "Jane", "Geoff"]],
         [{"name": "Gregg", "data": [1, 2, 3]},
          {"name": "Jane", "data": [4, 5, 6]},
          {"name": "Geoff", "data": [7, 8, 9]}],
         None),
        ([[[1, 2, 3], [4, 5, 6], [7, 8, 9]], "Gregg"],
         [{"name": "Gregg", "data": [1, 2, 3]},
          {"name": "Jane", "data": [4, 5, 6]},
          {"name": "Geoff", "data": [7, 8, 9]}],
         TypeError),
        ([[[1, 2, 3], [4, 5, 6], [7, 8, 9]], ["Gregg", "Jane"]],
         [{"name": "Gregg", "data": [1, 2, 3]},
          {"name": "Jane", "data": [4, 5, 6]},
          {"name": "Geoff", "data": [7, 8, 9]}],
         ValueError),
    ]
)
def test_attach_names(test, expected, expect_raises):
    """Test name attachment works for an array of data and raises exceptions
    for unexpected type and length mismatch."""
    from inflammation.models import attach_names
    if isinstance(test[0], list):
        test[0] = np.array(test[0])
    if expect_raises is not None:
        with pytest.raises(expect_raises):
            patients = attach_names(*test)
            npt.assert_array_equal(np.array([patient["data"] for patient in patients]), test[0])
            assert [patient["name"] for patient in patients] == test[1]
    else:
        patients = attach_names(*test)
        npt.assert_array_equal(np.array([patient["data"] for patient in patients]), test[0])
        assert [patient["name"] for patient in patients] == test[1]