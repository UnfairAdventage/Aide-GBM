import math
import numpy as np

def calculate_angular_frequency(k: int, n: int, N: int) -> float:
    """Calculates the angular frequency for Fourier analysis.

    Args:
        k: The frequency index.
        n: The current day index.
        N: The total number of days.

    Returns:
        The angular frequency in radians.
    """
    # Note: The formula in README uses 'n' from 1 to N. In code, we use 0-indexed arrays,
    # so the day index is n (0 to N-1), which corresponds to the n+1 day.
    # The formula should be 2 * pi * k * (n+1) / N for 0-indexed n, but given the README
    # formula uses n/N and sums from n=1 to N, let's stick to the README formula's structure
    # using 0-indexed n for data access but (n+1) for the angle calculation to match the sum from 1 to N.
    return 2 * math.pi * k * (n + 1) / N

def calculate_fourier_coefficients(data: list[float], N: int) -> tuple[list[float], list[float], list[float]]:
    """Calculates the standard Fourier coefficients (a_k, b_k, A_k) for the given data (k from 0 to N//2).

    Args:
        data: A list of numerical data points (e.g., daily GB values).
        N: The total number of data points (number of days).

    Returns:
        A tuple containing three lists: a_k coefficients, b_k coefficients, and A_k coefficients.
    """
    a_k = []
    b_k = []
    A_k = []
    # We calculate coefficients up to N/2 according to common Fourier analysis practice
    # For k=0, a_0 is the average and b_0 is 0. A_0 = a_0
    # For k > 0 and k < N/2, we calculate a_k, b_k, and A_k
    # For k = N/2 (if N is even), b_k is 0.
    for k in range(N // 2 + 1):
        sum_ak = 0.0
        sum_bk = 0.0
        for n in range(N):
            # Use 0-indexed n for data access, (n+1) for angle calculation to match README formula sum from 1 to N
            f = calculate_angular_frequency(k, n, N)
            sum_ak += data[n] * math.cos(f)
            sum_bk += data[n] * math.sin(f)

        ak = (2 / N) * sum_ak
        bk = (2 / N) * sum_bk
        Ak = math.sqrt(ak**2 + bk**2)

        a_k.append(ak)
        b_k.append(bk)
        A_k.append(Ak)

    return a_k, b_k, A_k

def calculate_specific_fourier_coefficients(data: list[float], N: int, max_k: int) -> tuple[list[int], list[float], list[float], list[float]]:
    """Calculates Fourier coefficients (a_k, b_k, A_k) for k from 1 up to max_k.

    Args:
        data: A list of numerical data points (e.g., daily GB values).
        N: The total number of data points (number of days).
        max_k: The maximum frequency index k to calculate coefficients for.

    Returns:
        A tuple containing four lists: k values, a_k coefficients, b_k coefficients, and A_k coefficients.
    """
    k_values = []
    a_k_values = []
    b_k_values = []
    A_k_values = []

    # Calculate coefficients for k from 1 up to max_k
    for k in range(1, max_k + 1):
        sum_ak = 0.0
        sum_bk = 0.0
        for n in range(N):
            # Use 0-indexed n for data access, (n+1) for angle calculation to match README formula sum from 1 to N
            angle = 2 * math.pi * k * (n + 1) / N
            sum_ak += data[n] * math.cos(angle)
            sum_bk += data[n] * math.sin(angle)

        ak = (2 / N) * sum_ak
        bk = (2 / N) * sum_bk
        Ak = math.sqrt(ak**2 + bk**2)

        k_values.append(k)
        a_k_values.append(ak)
        b_k_values.append(bk)
        A_k_values.append(Ak)

    return k_values, a_k_values, b_k_values, A_k_values

def calculate_log_transformations(k_values: list[int], A_k_values: list[float]) -> tuple[list[float], list[float]]:
    """Calculates the logarithmic transformations (x = log10(k), y = log10(A_k)).

    Args:
        k_values: A list of frequency indices k.
        A_k_values: A list of A_k coefficients.

    Returns:
        A tuple containing two lists: log10(k) values and log10(A_k) values.
    """
    x_values = []
    y_values = []
    for k, Ak in zip(k_values, A_k_values):
        # Avoid log10(0) for k=0 or A_k=0
        if k > 0 and Ak > 0:
            x_values.append(math.log10(k))
            y_values.append(math.log10(Ak))
        # The new calculate_specific_fourier_coefficients function starts k from 1,
        # so we don't need to explicitly handle k=0 here based on the new workflow.
        # However, the check for Ak > 0 is still necessary.
        elif Ak <= 0:
            # Handle Ak <= 0 case, log10 is undefined or -inf. Append a placeholder.
            x_values.append(math.log10(k)) # k is > 0 here
            y_values.append(float('-inf')) # Use -inf for log10(0) or log10 of small positive numbers approaching 0

    return x_values, y_values 