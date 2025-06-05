import math

def calculate_mean(data: list[float]) -> float:
    """Calculates the arithmetic mean of a list of numbers.

    Args:
        data: A list of numerical data points.

    Returns:
        The calculated mean.

    Raises:
        ValueError: If the input list is empty.
    """
    if not data:
        raise ValueError("Input list cannot be empty")
    return sum(data) / len(data)

def calculate_std_dev(data: list[float], mean: float) -> float:
    """Calculates the standard deviation of a list of numbers.

    Args:
        data: A list of numerical data points.
        mean: The mean of the data.

    Returns:
        The calculated standard deviation.

    Raises:
        ValueError: If the input list is empty.
    """
    if not data:
        raise ValueError("Input list cannot be empty")
    variance = sum([(x - mean) ** 2 for x in data]) / len(data)
    return math.sqrt(variance)

def calculate_regression_slope(x_values: list[float], y_values: list[float], N: int) -> float:
    """Calculates the slope (alpha) of the linear regression line.

    Args:
        x_values: A list of x-values.
        y_values: A list of y-values.
        N: The number of data points.

    Returns:
        The calculated slope (alpha).

    Raises:
        ValueError: If the number of data points is zero or if the lengths of x_values and y_values do not match N.
        ZeroDivisionError: If the denominator is zero, indicating a vertical line.
    """
    if N == 0 or len(x_values) != N or len(y_values) != N:
        raise ValueError("Invalid input: N must be greater than 0, and list lengths must match N")

    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum([x * y for x, y in zip(x_values, y_values)])
    sum_x_squared = sum([x ** 2 for x in x_values])

    denominator = N * sum_x_squared - sum_x ** 2
    if denominator == 0:
        raise ZeroDivisionError("Denominator is zero, cannot calculate slope (vertical line).")

    alpha = (N * sum_xy - sum_x * sum_y) / denominator
    return alpha

def calculate_regression_intercept(x_values: list[float], y_values: list[float], alpha: float, N: int) -> float:
    """Calculates the y-intercept (C) of the linear regression line.

    Args:
        x_values: A list of x-values.
        y_values: A list of y-values.
        alpha: The slope of the regression line.
        N: The number of data points.

    Returns:
        The calculated y-intercept (C).

    Raises:
        ValueError: If the number of data points is zero or if the lengths of x_values and y_values do not match N.
    """
    if N == 0 or len(x_values) != N or len(y_values) != N:
        raise ValueError("Invalid input: N must be greater than 0, and list lengths must match N")

    mean_x = calculate_mean(x_values)
    mean_y = calculate_mean(y_values)
    C = mean_y - alpha * mean_x
    return C

def calculate_correlation_coefficient(x_values: list[float], y_values: list[float], N: int) -> float:
    """Calculates the Pearson correlation coefficient (r).

    Args:
        x_values: A list of x-values.
        y_values: A list of y-values.
        N: The number of data points.

    Returns:
        The calculated correlation coefficient (r).

    Raises:
        ValueError: If the number of data points is less than 2 or if the lengths of x_values and y_values do not match N.
        ZeroDivisionError: If the standard deviation of x or y is zero.
    """
    if N < 2 or len(x_values) != N or len(y_values) != N:
        raise ValueError("Invalid input: N must be at least 2, and list lengths must match N")

    mean_x = calculate_mean(x_values)
    mean_y = calculate_mean(y_values)
    std_dev_x = calculate_std_dev(x_values, mean_x)
    std_dev_y = calculate_std_dev(y_values, mean_y)

    if std_dev_x == 0 or std_dev_y == 0:
        raise ZeroDivisionError("Standard deviation of x or y is zero, cannot calculate correlation coefficient.")

    sum_xy = sum([x * y for x, y in zip(x_values, y_values)])
    r = (sum_xy / N - mean_x * mean_y) / (std_dev_x * std_dev_y)
    return r 