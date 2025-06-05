#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Herramientas matemáticas para el cálculo de criticalidad metabólica.
"""

from typing import List, Tuple, Dict
import numpy as np
from dataclasses import dataclass

@dataclass
class StatisticalAnalysis:
    """Clase para almacenar resultados del análisis estadístico."""
    mean_x: float
    mean_y: float
    variance_x: float
    variance_y: float
    correlation: float
    xy_sum: float
    x2_sum: float
    y2_sum: float

def calculate_activity_factor(minutes: float) -> float:
    """
    Calcula el factor de actividad física basado en minutos de ejercicio.
    Args:
        minutes (float): Minutos de ejercicio
    Returns:
        float: Factor de actividad física
    """
    return 1.2 + 0.01 * minutes

def calculate_fourier_coefficients(x_n: List[float], k: int) -> Tuple[float, float, float, float]:
    """
    Calcula los coeficientes de Fourier para una serie de datos.
    Args:
        x_n (List[float]): Serie de datos
        k (int): Frecuencia
    Returns:
        Tuple[float, float, float, float]: Coeficientes (a_k, b_k, Ak, log10(Ak))
    """
    n = len(x_n)
    if n == 0:
        return 0.0, 0.0, 0.0, 0.0
    x_array = np.array(x_n)
    N = n
    n_array = np.arange(1, N + 1)
    a_k = (2/N) * np.sum(x_array * np.cos(2 * np.pi * k * n_array / N))
    b_k = (2/N) * np.sum(x_array * np.sin(2 * np.pi * k * n_array / N))
    Ak = np.sqrt(a_k**2 + b_k**2)
    log10_Ak = np.log10(Ak) if Ak > 0 else 0.0
    return a_k, b_k, Ak, log10_Ak

def calculate_statistics(x: List[float], y: List[float]) -> StatisticalAnalysis:
    """
    Calcula estadísticas básicas para dos series de datos.
    
    Args:
        x (List[float]): Primera serie de datos
        y (List[float]): Segunda serie de datos
        
    Returns:
        StatisticalAnalysis: Objeto con los resultados estadísticos
    """
    x_array = np.array(x)
    y_array = np.array(y)
    
    mean_x = np.mean(x_array)
    mean_y = np.mean(y_array)
    
    variance_x = np.var(x_array)
    variance_y = np.var(y_array)
    
    xy_sum = np.sum(x_array * y_array)
    x2_sum = np.sum(x_array ** 2)
    y2_sum = np.sum(y_array ** 2)
    
    # Correlación de Pearson
    correlation = np.corrcoef(x_array, y_array)[0, 1]
    
    return StatisticalAnalysis(
        mean_x=mean_x,
        mean_y=mean_y,
        variance_x=variance_x,
        variance_y=variance_y,
        correlation=correlation,
        xy_sum=xy_sum,
        x2_sum=x2_sum,
        y2_sum=y2_sum
    )

def calculate_fourier_table(x_n: List[float], k: int) -> List[Dict[str, float]]:
    """
    Genera una tabla con los cálculos de Fourier para cada punto.
    Args:
        x_n (List[float]): Serie de datos
        k (int): Frecuencia
    Returns:
        List[Dict[str, float]]: Lista de diccionarios con los cálculos
    """
    n = len(x_n)
    if n == 0:
        return []
    N = n
    table = []
    for i, x in enumerate(x_n, 1):
        cos_term = np.cos(2 * np.pi * k * i / N)
        sin_term = np.sin(2 * np.pi * k * i / N)
        table.append({
            'n': i,
            'x': x,
            'cos': cos_term,
            'sin': sin_term,
            'x_cos': x * cos_term,
            'x_sin': x * sin_term
        })
    return table 