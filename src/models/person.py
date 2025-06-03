#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo para almacenar y calcular datos personales relacionados con el gasto metabólico.
"""

from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass
class Person:
    """Clase que representa a una persona y sus datos metabólicos."""
    
    sex: str  # 'M' o 'F'
    weight: float  # en kg
    height: float  # en cm
    age: int  # en años
    exercise_minutes: List[float]  # lista de minutos de ejercicio por día
    
    def calculate_bmr(self) -> float:
        """
        Calcula el Gasto Metabólico Basal (TMB) usando la fórmula de Harris-Benedict.
        
        Returns:
            float: Valor del TMB en kcal/día
        """
        if self.sex.upper() == 'M':
            return 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            return 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.333 * self.age)
    
    def calculate_daily_expenditure(self) -> List[float]:
        """
        Calcula el gasto bruto diario (GB) para cada día.
        
        Returns:
            List[float]: Lista de gastos brutos diarios
        """
        bmr = self.calculate_bmr()
        return [bmr + minutes for minutes in self.exercise_minutes]
    
    def calculate_fourier_coefficients(self, k: int) -> tuple:
        """
        Calcula los coeficientes de Fourier para una frecuencia k dada.
        
        Args:
            k (int): Frecuencia para el cálculo
            
        Returns:
            tuple: (a_k, b_k) coeficientes de Fourier
        """
        n = len(self.exercise_minutes)
        if n == 0:
            return 0.0, 0.0
            
        x_n = np.array(self.calculate_daily_expenditure())
        n_array = np.arange(1, n + 1)
        
        a_k = (2/n) * np.sum(x_n * np.cos(2 * np.pi * k * n_array / n))
        b_k = (2/n) * np.sum(x_n * np.sin(2 * np.pi * k * n_array / n))
        
        return a_k, b_k 