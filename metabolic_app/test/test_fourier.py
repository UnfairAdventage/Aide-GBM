import pytest
import math
from src.models.fourier import calculate_angular_frequency, calculate_fourier_coefficients, calculate_log_transformations

def test_calculate_angular_frequency():
    """Tests the calculate_angular_frequency function."""
    k = 1
    n = 5
    N = 10
    expected_f = 2 * math.pi * k * n / N
    assert calculate_angular_frequency(k, n, N) == pytest.approx(expected_f)

def test_calculate_fourier_coefficients():
    """Tests the calculate_fourier_coefficients function with a simple dataset."""
    data = [10.0, 20.0, 30.0, 40.0]
    N = len(data)

    # Expected values calculated manually or from a known source for this simple case
    # This is a simplified test; real-world data would require more robust test cases.
    # For N=4, k goes from 0 to N//2 = 2

    # k=0
    # f = 2*pi*0*n/4 = 0
    # a_0 = (2/4) * sum(data * cos(0)) = 0.5 * sum(data) = 0.5 * (10+20+30+40) = 0.5 * 100 = 50
    # b_0 = (2/4) * sum(data * sin(0)) = 0.5 * sum(data * 0) = 0
    # A_0 = sqrt(a_0^2 + b_0^2) = sqrt(50^2 + 0^2) = 50

    # k=1
    # n=0, f=0, cos(0)=1, sin(0)=0
    # n=1, f=pi/2, cos(pi/2)=0, sin(pi/2)=1
    # n=2, f=pi, cos(pi)=-1, sin(pi)=0
    # n=3, f=3pi/2, cos(3pi/2)=0, sin(3pi/2)=-1
    # sum_ak = data[0]*1 + data[1]*0 + data[2]*-1 + data[3]*0 = 10 - 30 = -20
    # a_1 = (2/4) * -20 = -10
    # sum_bk = data[0]*0 + data[1]*1 + data[2]*0 + data[3]*-1 = 20 - 40 = -20
    # b_1 = (2/4) * -20 = -10
    # A_1 = sqrt((-10)^2 + (-10)^2) = sqrt(100 + 100) = sqrt(200) approx 14.1421

    # k=2
    # n=0, f=0, cos(0)=1, sin(0)=0
    # n=1, f=pi, cos(pi)=-1, sin(pi)=0
    # n=2, f=2pi, cos(2pi)=1, sin(2pi)=0
    # n=3, f=3pi, cos(3pi)=-1, sin(3pi)=0
    # sum_ak = data[0]*1 + data[1]*-1 + data[2]*1 + data[3]*-1 = 10 - 20 + 30 - 40 = -20
    # a_2 = (2/4) * -20 = -10
    # sum_bk = data[0]*0 + data[1]*0 + data[2]*0 + data[3]*0 = 0
    # b_2 = (2/4) * 0 = 0
    # A_2 = sqrt((-10)^2 + 0^2) = sqrt(100) = 10

    expected_a_k = [50.0, -10.0, -10.0]
    expected_b_k = [0.0, -10.0, 0.0]
    expected_A_k = [50.0, math.sqrt(200), 10.0]

    a_k, b_k, A_k = calculate_fourier_coefficients(data, N)

    assert a_k == pytest.approx(expected_a_k)
    assert b_k == pytest.approx(expected_b_k)
    assert A_k == pytest.approx(expected_A_k)

def test_calculate_log_transformations():
    """Tests the calculate_log_transformations function."""
    k_values = [1, 2, 3]
    A_k_values = [10.0, 20.0, 30.0]

    expected_log10_k = [math.log10(1), math.log10(2), math.log10(3)]
    expected_log10_A_k = [math.log10(10), math.log10(20), math.log10(30)]

    log10_k, log10_A_k = calculate_log_transformations(k_values, A_k_values)

    assert log10_k == pytest.approx(expected_log10_k)
    assert log10_A_k == pytest.approx(expected_log10_A_k)

def test_calculate_log_transformations_with_zero():
    """Tests log transformations with k=0 or A_k=0, which should be skipped."""
    k_values = [0, 1, 2]
    A_k_values = [5.0, 10.0, 0.0]

    # k=0 should be skipped, A_k=0 should be skipped
    expected_log10_k = [math.log10(1)]
    expected_log10_A_k = [math.log10(10)]

    log10_k, log10_A_k = calculate_log_transformations(k_values, A_k_values)

    assert log10_k == pytest.approx(expected_log10_k)
    assert log10_A_k == pytest.approx(expected_log10_A_k) 