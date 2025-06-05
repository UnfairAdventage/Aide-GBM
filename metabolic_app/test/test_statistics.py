import pytest
import math
from src.models.statistics import calculate_mean, calculate_std_dev, calculate_regression_slope, calculate_regression_intercept, calculate_correlation_coefficient

def test_calculate_mean():
    """Tests the calculate_mean function."""
    data = [1, 2, 3, 4, 5]
    expected_mean = 3.0
    assert calculate_mean(data) == pytest.approx(expected_mean)

def test_calculate_mean_empty():
    """Tests the calculate_mean function with an empty list."""
    with pytest.raises(ValueError):
        calculate_mean([])

def test_calculate_std_dev():
    """Tests the calculate_std_dev function."""
    data = [1, 2, 3, 4, 5]
    mean = 3.0
    # Population standard deviation formula used in statistics.py
    variance = sum([(x - mean) ** 2 for x in data]) / len(data)
    expected_std_dev = math.sqrt(variance)
    assert calculate_std_dev(data, mean) == pytest.approx(expected_std_dev)

def test_calculate_std_dev_empty():
    """Tests the calculate_std_dev function with an empty list."""
    with pytest.raises(ValueError):
        calculate_std_dev([], 0.0)

def test_calculate_regression_slope():
    """Tests the calculate_regression_slope function."""
    x_values = [1, 2, 3, 4, 5]
    y_values = [2, 4, 5, 4, 5]
    N = len(x_values)
    # Expected values calculated using a standard statistical tool or formula
    # For these values, the slope should be close to 0.6
    expected_alpha = 0.6
    assert calculate_regression_slope(x_values, y_values, N) == pytest.approx(expected_alpha)

def test_calculate_regression_slope_vertical_line():
    """Tests the calculate_regression_slope function with data that forms a vertical line."""
    x_values = [1, 1, 1, 1]
    y_values = [1, 2, 3, 4]
    N = len(x_values)
    with pytest.raises(ZeroDivisionError):
        calculate_regression_slope(x_values, y_values, N)

def test_calculate_regression_intercept():
    """Tests the calculate_regression_intercept function."""
    x_values = [1, 2, 3, 4, 5]
    y_values = [2, 4, 5, 4, 5]
    N = len(x_values)
    alpha = 0.6 # Assuming the calculated slope is 0.6
    # Expected value calculated using mean_y - alpha * mean_x
    mean_x = sum(x_values) / N
    mean_y = sum(y_values) / N
    expected_c = mean_y - alpha * mean_x
    assert calculate_regression_intercept(x_values, y_values, alpha, N) == pytest.approx(expected_c)

def test_calculate_correlation_coefficient():
    """Tests the calculate_correlation_coefficient function."""
    x_values = [1, 2, 3, 4, 5]
    y_values = [2, 4, 5, 4, 5]
    N = len(x_values)
    # Expected value calculated manually:
    # x_mean = 3, y_mean = 4
    # x_diff = [-2, -1, 0, 1, 2]
    # y_diff = [-2, 0, 1, 0, 1]
    # covariance = (4 + 0 + 0 + 0 + 2) / 5 = 1.2
    # x_std = sqrt(10/5) = sqrt(2)
    # y_std = sqrt(6/5)
    # r = 1.2 / (sqrt(2) * sqrt(6/5)) ≈ 0.7746
    expected_r = 0.7745966692414833
    assert calculate_correlation_coefficient(x_values, y_values, N) == pytest.approx(expected_r)

def test_calculate_correlation_coefficient_zero_std_dev():
    """Tests the calculate_correlation_coefficient function with zero standard deviation."""
    x_values = [1, 1, 1, 1]
    y_values = [1, 2, 3, 4]
    N = len(x_values)
    with pytest.raises(ZeroDivisionError):
        calculate_correlation_coefficient(x_values, y_values, N) 