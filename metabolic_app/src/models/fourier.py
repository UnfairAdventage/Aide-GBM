import math
import numpy as np

def calculate_angular_frequency(k: int, n: int, N: int) -> float:
    """
    Calcula la frecuencia angular para un valor dado de k, n y N.
    
    Args:
        k: Número de onda
        n: Índice de tiempo
        N: Número total de puntos
        
    Returns:
        float: Frecuencia angular
    """
    return 2 * math.pi * k * n / N

def calculate_fourier_coefficients(data: list[float], N: int) -> tuple[list[float], list[float], list[float]]:
    """
    Calcula los coeficientes de Fourier para una serie de datos.
    
    Args:
        data: Lista de valores de datos
        N: Número total de puntos
        
    Returns:
        tuple: (a_k, b_k, A_k) donde:
            - a_k: Coeficientes coseno
            - b_k: Coeficientes seno
            - A_k: Amplitudes
    """
    a_k = []
    b_k = []
    A_k = []
    
    # Para cada k desde 0 hasta N//2
    for k in range(N // 2 + 1):
        sum_ak = 0.0
        sum_bk = 0.0
        
        # Calcular sumas para a_k y b_k
        for n in range(N):
            f = calculate_angular_frequency(k, n, N)
            sum_ak += data[n] * math.cos(f)
            sum_bk += data[n] * math.sin(f)
        
        # Calcular coeficientes finales
        a_k.append((2.0 / N) * sum_ak)
        b_k.append((2.0 / N) * sum_bk)
        A_k.append(math.sqrt(a_k[-1]**2 + b_k[-1]**2))
    
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
    """
    Calcula las transformaciones logarítmicas de k y A_k.
    
    Args:
        k_values: Lista de valores de k
        A_k_values: Lista de valores de A_k
        
    Returns:
        tuple: (log10_k, log10_A_k) donde:
            - log10_k: Logaritmo base 10 de k
            - log10_A_k: Logaritmo base 10 de A_k
    """
    log10_k = []
    log10_A_k = []
    
    for k, A_k in zip(k_values, A_k_values):
        # Skip k=0 and A_k=0
        if k == 0 or A_k == 0:
            continue
        log10_k.append(math.log10(k))
        log10_A_k.append(math.log10(A_k))
    
    return log10_k, log10_A_k 